"use client";

/**
 * 👥 Team Management Component
 * Manage team members, roles, and permissions
 */

import React, { useState } from 'react';
import { useToast } from '../ui/Toast';
import { ModalTransition } from '../ui/Transitions';

export type TeamRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: TeamRole;
  avatar?: string;
  joinedAt: string;
  lastActive: string;
  status: 'active' | 'pending' | 'inactive';
}

interface TeamManagementProps {
  teamId?: string;
  currentUserId?: string;
}

/**
 * Main Team Management Component
 */
export const TeamManagement: React.FC<TeamManagementProps> = ({
  teamId = 'demo',
  currentUserId = 'user1',
}) => {
  const { success, error, warning } = useToast();
  const [members, setMembers] = useState<TeamMember[]>([
    {
      id: 'user1',
      name: 'You',
      email: 'you@example.com',
      role: 'owner',
      joinedAt: '2025-01-01',
      lastActive: '2025-12-03',
      status: 'active',
    },
    {
      id: 'user2',
      name: 'Alice Johnson',
      email: 'alice@example.com',
      role: 'admin',
      joinedAt: '2025-01-15',
      lastActive: '2025-12-02',
      status: 'active',
    },
    {
      id: 'user3',
      name: 'Bob Smith',
      email: 'bob@example.com',
      role: 'member',
      joinedAt: '2025-02-01',
      lastActive: '2025-11-30',
      status: 'active',
    },
    {
      id: 'user4',
      name: 'Charlie Brown',
      email: 'charlie@example.com',
      role: 'viewer',
      joinedAt: '2025-02-15',
      lastActive: 'Never',
      status: 'pending',
    },
  ]);

  const [showInviteModal, setShowInviteModal] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<TeamRole>('member');

  const handleInvite = () => {
    if (!inviteEmail) {
      warning('Please enter an email address');
      return;
    }

    // TODO: Actual API call to send invitation
    success(`Invitation sent to ${inviteEmail}`, 'They will receive an email shortly.');

    setMembers([
      ...members,
      {
        id: `user${members.length + 1}`,
        name: inviteEmail.split('@')[0],
        email: inviteEmail,
        role: inviteRole,
        joinedAt: new Date().toISOString().split('T')[0],
        lastActive: 'Never',
        status: 'pending',
      },
    ]);

    setInviteEmail('');
    setInviteRole('member');
    setShowInviteModal(false);
  };

  const handleRemoveMember = (memberId: string) => {
    const member = members.find((m) => m.id === memberId);
    if (!member) return;

    if (member.role === 'owner') {
      error('Cannot remove owner', 'Transfer ownership first.');
      return;
    }

    // TODO: Actual API call
    setMembers(members.filter((m) => m.id !== memberId));
    success(`Removed ${member.name} from team`);
  };

  const handleChangeRole = (memberId: string, newRole: TeamRole) => {
    const member = members.find((m) => m.id === memberId);
    if (!member) return;

    // TODO: Actual API call
    setMembers(
      members.map((m) => (m.id === memberId ? { ...m, role: newRole } : m))
    );
    success(`Changed ${member.name}'s role to ${newRole}`);
  };

  const handleResendInvite = (memberId: string) => {
    const member = members.find((m) => m.id === memberId);
    if (!member) return;

    // TODO: Actual API call
    success(`Invitation resent to ${member.email}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Team Management</h2>
          <p className="text-gray-400">
            Manage your team members and their permissions
          </p>
        </div>
        <button
          onClick={() => setShowInviteModal(true)}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105"
        >
          + Invite Member
        </button>
      </div>

      {/* Team Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard icon="👥" label="Total Members" value={members.length.toString()} />
        <StatCard
          icon="✅"
          label="Active"
          value={members.filter((m) => m.status === 'active').length.toString()}
        />
        <StatCard
          icon="⏳"
          label="Pending"
          value={members.filter((m) => m.status === 'pending').length.toString()}
        />
        <StatCard
          icon="👑"
          label="Admins"
          value={members.filter((m) => m.role === 'admin' || m.role === 'owner').length.toString()}
        />
      </div>

      {/* Members Table */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-900">
            <tr>
              <th className="text-left px-6 py-4 text-gray-400 font-medium">Member</th>
              <th className="text-left px-6 py-4 text-gray-400 font-medium">Role</th>
              <th className="text-left px-6 py-4 text-gray-400 font-medium">Status</th>
              <th className="text-left px-6 py-4 text-gray-400 font-medium">Last Active</th>
              <th className="text-right px-6 py-4 text-gray-400 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {members.map((member) => (
              <tr key={member.id} className="hover:bg-gray-900/50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
                      {member.name[0].toUpperCase()}
                    </div>
                    <div>
                      <div className="font-medium text-white">{member.name}</div>
                      <div className="text-sm text-gray-400">{member.email}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <RoleSelector
                    currentRole={member.role}
                    onChange={(newRole) => handleChangeRole(member.id, newRole)}
                    disabled={member.id === currentUserId || member.role === 'owner'}
                  />
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={member.status} />
                </td>
                <td className="px-6 py-4 text-gray-400">
                  {member.lastActive === 'Never' ? (
                    <span className="text-gray-500">Never</span>
                  ) : (
                    new Date(member.lastActive).toLocaleDateString()
                  )}
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    {member.status === 'pending' && (
                      <button
                        onClick={() => handleResendInvite(member.id)}
                        className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                      >
                        Resend Invite
                      </button>
                    )}
                    {member.id !== currentUserId && member.role !== 'owner' && (
                      <button
                        onClick={() => handleRemoveMember(member.id)}
                        className="px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Invite Modal */}
      <ModalTransition isOpen={showInviteModal} onClose={() => setShowInviteModal(false)}>
        <div className="bg-gray-800 rounded-xl p-8 max-w-md w-full border border-gray-700">
          <h3 className="text-2xl font-bold text-white mb-6">Invite Team Member</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={inviteEmail}
                onChange={(e) => setInviteEmail(e.target.value)}
                placeholder="colleague@example.com"
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Role
              </label>
              <select
                value={inviteRole}
                onChange={(e) => setInviteRole(e.target.value as TeamRole)}
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="viewer">Viewer - Read-only access</option>
                <option value="member">Member - Can use APIs</option>
                <option value="admin">Admin - Can manage team</option>
              </select>
            </div>
          </div>

          <div className="flex gap-3 mt-6">
            <button
              onClick={handleInvite}
              className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            >
              Send Invitation
            </button>
            <button
              onClick={() => setShowInviteModal(false)}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </ModalTransition>
    </div>
  );
};

/**
 * Role Selector Component
 */
const RoleSelector: React.FC<{
  currentRole: TeamRole;
  onChange: (role: TeamRole) => void;
  disabled?: boolean;
}> = ({ currentRole, onChange, disabled = false }) => {
  const roleColors: Record<TeamRole, string> = {
    owner: 'bg-purple-600',
    admin: 'bg-blue-600',
    member: 'bg-green-600',
    viewer: 'bg-gray-600',
  };

  if (disabled) {
    return (
      <span className={`px-3 py-1 ${roleColors[currentRole]} text-white text-sm rounded-full`}>
        {currentRole}
      </span>
    );
  }

  return (
    <select
      value={currentRole}
      onChange={(e) => onChange(e.target.value as TeamRole)}
      className="px-3 py-1 bg-gray-900 border border-gray-700 text-white text-sm rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="viewer">Viewer</option>
      <option value="member">Member</option>
      <option value="admin">Admin</option>
    </select>
  );
};

/**
 * Status Badge Component
 */
const StatusBadge: React.FC<{ status: 'active' | 'pending' | 'inactive' }> = ({ status }) => {
  const colors = {
    active: 'bg-green-900/30 text-green-400 border-green-500/30',
    pending: 'bg-yellow-900/30 text-yellow-400 border-yellow-500/30',
    inactive: 'bg-gray-700/30 text-gray-400 border-gray-600/30',
  };

  const icons = {
    active: '✓',
    pending: '⏳',
    inactive: '○',
  };

  return (
    <span
      className={`inline-flex items-center gap-1 px-3 py-1 text-sm rounded-full border ${colors[status]}`}
    >
      {icons[status]} {status}
    </span>
  );
};

/**
 * Stat Card Component
 */
const StatCard: React.FC<{ icon: string; label: string; value: string }> = ({
  icon,
  label,
  value,
}) => (
  <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
    <div className="flex items-center gap-2 mb-2">
      <span className="text-2xl">{icon}</span>
      <span className="text-gray-400 text-sm">{label}</span>
    </div>
    <div className="text-2xl font-bold text-white">{value}</div>
  </div>
);

export default TeamManagement;
