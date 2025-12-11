"""
🏢 Team Management API
Handles teams, workspaces, invitations, and RBAC

VILLAIN ORGANIZATIONS: ASSEMBLE YOUR CREW 😈
"""

import secrets
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..database import (Team, TeamInvitation, TeamMember, User, get_db)

router = APIRouter()

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TeamCreate(BaseModel):
    name: str
    slug: str

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    settings: Optional[dict] = None

class TeamResponse(BaseModel):
    id: str
    name: str
    slug: str
    owner_id: str
    subscription_tier: str
    subscription_status: str
    created_at: datetime
    member_count: int

    class Config:
        from_attributes = True

class InviteMember(BaseModel):
    email: EmailStr
    role: str = "member"  # admin, member, viewer

class TeamMemberResponse(BaseModel):
    id: str
    user_id: str
    role: str
    joined_at: datetime
    user_email: Optional[str] = None
    user_name: Optional[str] = None

    class Config:
        from_attributes = True

class InvitationResponse(BaseModel):
    id: str
    email: str
    role: str
    status: str
    created_at: datetime
    expires_at: datetime
    invited_by: str

    class Config:
        from_attributes = True

# ============================================================================
# RBAC PERMISSIONS
# ============================================================================

ROLE_PERMISSIONS = {
    "owner": [
        "team:read",
        "team:update",
        "team:delete",
        "members:invite",
        "members:remove",
        "members:update_role",
        "billing:manage",
        "settings:manage"
    ],
    "admin": [
        "team:read",
        "team:update",
        "members:invite",
        "members:remove",
        "settings:manage"
    ],
    "member": [
        "team:read",
        "agents:use",
        "dashboard:view"
    ],
    "viewer": [
        "team:read",
        "dashboard:view"
    ]
}

def check_permission(role: str, permission: str) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_user(db: Session, user_id: str) -> User:
    """Get current user from database"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_team_member(db: Session, team_id: str, user_id: str) -> TeamMember:
    """Get team membership for a user"""
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this team")
    return member

def verify_permission(member: TeamMember, permission: str):
    """Verify user has required permission"""
    if not check_permission(member.role, permission):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: {permission} required"
        )

# ============================================================================
# TEAM CRUD ENDPOINTS
# ============================================================================

@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    🏢 Create a new team/workspace

    The creator becomes the owner
    """
    # Check if slug is available
    existing_team = db.query(Team).filter(Team.slug == team_data.slug).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team slug already taken")

    # Create team
    team = Team(
        id=str(uuid.uuid4()),
        name=team_data.name,
        slug=team_data.slug,
        owner_id=user_id,
        subscription_tier="free",
        subscription_status="active"
    )
    db.add(team)

    # Add creator as owner
    member = TeamMember(
        id=str(uuid.uuid4()),
        team_id=team.id,
        user_id=user_id,
        role="owner"
    )
    db.add(member)

    db.commit()
    db.refresh(team)

    return TeamResponse(
        id=team.id,
        name=team.name,
        slug=team.slug,
        owner_id=team.owner_id,
        subscription_tier=team.subscription_tier,
        subscription_status=team.subscription_status,
        created_at=team.created_at,
        member_count=1
    )

@router.get("/teams", response_model=List[TeamResponse])
async def list_teams(
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    📋 List all teams the user is a member of
    """
    # Get all team memberships for user
    memberships = db.query(TeamMember).filter(TeamMember.user_id == user_id).all()

    teams = []
    for membership in memberships:
        team = db.query(Team).filter(Team.id == membership.team_id).first()
        if team:
            member_count = db.query(TeamMember).filter(TeamMember.team_id == team.id).count()
            teams.append(TeamResponse(
                id=team.id,
                name=team.name,
                slug=team.slug,
                owner_id=team.owner_id,
                subscription_tier=team.subscription_tier,
                subscription_status=team.subscription_status,
                created_at=team.created_at,
                member_count=member_count
            ))

    return teams

@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    🔍 Get team details
    """
    # Verify membership
    member = get_team_member(db, team_id, user_id)

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    member_count = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()

    return TeamResponse(
        id=team.id,
        name=team.name,
        slug=team.slug,
        owner_id=team.owner_id,
        subscription_tier=team.subscription_tier,
        subscription_status=team.subscription_status,
        created_at=team.created_at,
        member_count=member_count
    )

@router.patch("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    team_data: TeamUpdate,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    ✏️ Update team details (owner/admin only)
    """
    member = get_team_member(db, team_id, user_id)
    verify_permission(member, "team:update")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Update fields
    if team_data.name:
        team.name = team_data.name
    if team_data.settings is not None:
        team.settings = team_data.settings

    team.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(team)

    member_count = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()

    return TeamResponse(
        id=team.id,
        name=team.name,
        slug=team.slug,
        owner_id=team.owner_id,
        subscription_tier=team.subscription_tier,
        subscription_status=team.subscription_status,
        created_at=team.created_at,
        member_count=member_count
    )

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    🗑️ Delete team (owner only)
    """
    member = get_team_member(db, team_id, user_id)
    verify_permission(member, "team:delete")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Delete all members and invitations
    db.query(TeamMember).filter(TeamMember.team_id == team_id).delete()
    db.query(TeamInvitation).filter(TeamInvitation.team_id == team_id).delete()

    # Delete team
    db.delete(team)
    db.commit()

    return None

# ============================================================================
# MEMBER MANAGEMENT
# ============================================================================

@router.get("/teams/{team_id}/members", response_model=List[TeamMemberResponse])
async def list_team_members(
    team_id: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    👥 List all team members
    """
    # Verify membership
    member = get_team_member(db, team_id, user_id)

    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()

    # Enrich with user data
    result = []
    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        result.append(TeamMemberResponse(
            id=m.id,
            user_id=m.user_id,
            role=m.role,
            joined_at=m.joined_at,
            user_email=user.email if user else None,
            user_name=user.name if user else None
        ))

    return result

@router.post("/teams/{team_id}/invitations", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    team_id: str,
    invite_data: InviteMember,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    ✉️ Invite a new member to the team
    """
    member = get_team_member(db, team_id, user_id)
    verify_permission(member, "members:invite")

    # Check if user is already a member
    invited_user = db.query(User).filter(User.email == invite_data.email).first()
    if invited_user:
        existing_member = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.user_id == invited_user.id
        ).first()
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member")

    # Check for pending invitation
    pending = db.query(TeamInvitation).filter(
        TeamInvitation.team_id == team_id,
        TeamInvitation.email == invite_data.email,
        TeamInvitation.status == "pending"
    ).first()
    if pending:
        raise HTTPException(status_code=400, detail="Invitation already sent")

    # Create invitation
    invitation = TeamInvitation(
        id=str(uuid.uuid4()),
        team_id=team_id,
        email=invite_data.email,
        role=invite_data.role,
        invited_by=user_id,
        expires_at=datetime.utcnow() + timedelta(days=7),
        token=secrets.token_urlsafe(32)
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    # TODO: Send invitation email

    return InvitationResponse(
        id=invitation.id,
        email=invitation.email,
        role=invitation.role,
        status=invitation.status,
        created_at=invitation.created_at,
        expires_at=invitation.expires_at,
        invited_by=invitation.invited_by
    )

@router.post("/teams/accept-invitation/{token}")
async def accept_invitation(
    token: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    ✅ Accept a team invitation
    """
    invitation = db.query(TeamInvitation).filter(TeamInvitation.token == token).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if invitation.status != "pending":
        raise HTTPException(status_code=400, detail="Invitation already processed")

    if invitation.expires_at < datetime.utcnow():
        invitation.status = "expired"
        db.commit()
        raise HTTPException(status_code=400, detail="Invitation expired")

    # Get user
    user = get_current_user(db, user_id)

    # Verify email matches
    if user.email != invitation.email:
        raise HTTPException(status_code=403, detail="Email mismatch")

    # Add as team member
    member = TeamMember(
        id=str(uuid.uuid4()),
        team_id=invitation.team_id,
        user_id=user_id,
        role=invitation.role,
        invited_by=invitation.invited_by
    )
    db.add(member)

    # Update invitation status
    invitation.status = "accepted"
    db.commit()

    return {
        "status": "success",
        "message": "Invitation accepted",
        "team_id": invitation.team_id
    }

@router.delete("/teams/{team_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    team_id: str,
    member_id: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    🚫 Remove a member from the team
    """
    member = get_team_member(db, team_id, user_id)
    verify_permission(member, "members:remove")

    # Get target member
    target = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Member not found")

    # Can't remove the owner
    if target.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot remove team owner")

    db.delete(target)
    db.commit()

    return None

@router.patch("/teams/{team_id}/members/{member_id}/role")
async def update_member_role(
    team_id: str,
    member_id: str,
    new_role: str,
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    🔄 Update a member's role
    """
    member = get_team_member(db, team_id, user_id)
    verify_permission(member, "members:update_role")

    # Get target member
    target = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Member not found")

    # Can't change the owner's role
    if target.role == "owner":
        raise HTTPException(status_code=400, detail="Cannot change owner's role")

    # Validate role
    if new_role not in ["admin", "member", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    target.role = new_role
    db.commit()

    return {
        "status": "success",
        "message": f"Role updated to {new_role}"
    }
