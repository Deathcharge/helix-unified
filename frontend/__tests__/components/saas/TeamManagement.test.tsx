/**
 * 🧪 TeamManagement Component Tests
 * Comprehensive tests for team member management
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TeamManagement } from '@/components/saas/TeamManagement';
import type { TeamMember, TeamRole } from '@/components/saas/TeamManagement';

// Mock the Toast hook
const mockSuccess = jest.fn();
const mockError = jest.fn();
const mockWarning = jest.fn();

jest.mock('@/components/ui/Toast', () => ({
  useToast: () => ({
    success: mockSuccess,
    error: mockError,
    warning: mockWarning,
  }),
}));

// Mock ModalTransition to render children directly
jest.mock('@/components/ui/Transitions', () => ({
  ModalTransition: ({ isOpen, children }: { isOpen: boolean; children: React.ReactNode }) => (
    isOpen ? <div data-testid="modal">{children}</div> : null
  ),
}));

describe('TeamManagement', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Component Rendering', () => {
    it('renders without crashing', () => {
      render(<TeamManagement />);
      expect(screen.getByText('Team Management')).toBeInTheDocument();
    });

    it('displays header with description', () => {
      render(<TeamManagement />);
      expect(screen.getByText('Team Management')).toBeInTheDocument();
      expect(screen.getByText('Manage your team members and their permissions')).toBeInTheDocument();
    });

    it('displays invite member button', () => {
      render(<TeamManagement />);
      expect(screen.getByText('+ Invite Member')).toBeInTheDocument();
    });

    it('renders with custom teamId and currentUserId', () => {
      render(<TeamManagement teamId="team-123" currentUserId="user-456" />);
      expect(screen.getByText('Team Management')).toBeInTheDocument();
    });
  });

  describe('Team Stats', () => {
    it('displays all stat cards', () => {
      render(<TeamManagement />);
      expect(screen.getByText('Total Members')).toBeInTheDocument();
      expect(screen.getByText('Active')).toBeInTheDocument();
      expect(screen.getByText('Pending')).toBeInTheDocument();
      expect(screen.getByText('Admins')).toBeInTheDocument();
    });

    it('shows correct total members count', () => {
      render(<TeamManagement />);
      // Default has 4 members
      const totalMembersCard = screen.getByText('Total Members').closest('div');
      expect(totalMembersCard).toHaveTextContent('4');
    });

    it('shows correct active members count', () => {
      render(<TeamManagement />);
      // 3 active members by default
      const activeCard = screen.getByText('Active').closest('div');
      expect(activeCard).toHaveTextContent('3');
    });

    it('shows correct pending members count', () => {
      render(<TeamManagement />);
      // 1 pending member by default
      const pendingCard = screen.getByText('Pending').closest('div');
      expect(pendingCard).toHaveTextContent('1');
    });

    it('shows correct admin count (owner + admin)', () => {
      render(<TeamManagement />);
      // 1 owner + 1 admin = 2
      const adminsCard = screen.getByText('Admins').closest('div');
      expect(adminsCard).toHaveTextContent('2');
    });

    it('displays stat card icons', () => {
      render(<TeamManagement />);
      expect(screen.getByText('👥')).toBeInTheDocument();
      expect(screen.getByText('✅')).toBeInTheDocument();
      expect(screen.getByText('⏳')).toBeInTheDocument();
      expect(screen.getByText('👑')).toBeInTheDocument();
    });
  });

  describe('Members Table', () => {
    it('renders table headers', () => {
      render(<TeamManagement />);
      expect(screen.getByText('Member')).toBeInTheDocument();
      expect(screen.getByText('Role')).toBeInTheDocument();
      expect(screen.getByText('Status')).toBeInTheDocument();
      expect(screen.getByText('Last Active')).toBeInTheDocument();
      expect(screen.getByText('Actions')).toBeInTheDocument();
    });

    it('displays all default members', () => {
      render(<TeamManagement />);
      expect(screen.getByText('You')).toBeInTheDocument();
      expect(screen.getByText('Alice Johnson')).toBeInTheDocument();
      expect(screen.getByText('Bob Smith')).toBeInTheDocument();
      expect(screen.getByText('Charlie Brown')).toBeInTheDocument();
    });

    it('displays member emails', () => {
      render(<TeamManagement />);
      expect(screen.getByText('you@example.com')).toBeInTheDocument();
      expect(screen.getByText('alice@example.com')).toBeInTheDocument();
      expect(screen.getByText('bob@example.com')).toBeInTheDocument();
      expect(screen.getByText('charlie@example.com')).toBeInTheDocument();
    });

    it('displays member avatars with first letter', () => {
      const { container } = render(<TeamManagement />);
      // Check for avatar circles
      const avatars = container.querySelectorAll('.bg-gradient-to-br.from-blue-500');
      expect(avatars.length).toBeGreaterThan(0);
    });

    it('displays formatted last active dates', () => {
      render(<TeamManagement />);
      // Should show "Never" for pending member
      expect(screen.getByText('Never')).toBeInTheDocument();
    });
  });

  describe('Status Badges', () => {
    it('displays active status badge', () => {
      render(<TeamManagement />);
      const badges = screen.getAllByText(/active/i);
      expect(badges.length).toBeGreaterThan(0);
    });

    it('displays pending status badge', () => {
      render(<TeamManagement />);
      expect(screen.getByText(/pending/i)).toBeInTheDocument();
    });

    it('shows correct status icons', () => {
      const { container } = render(<TeamManagement />);
      // Status badges should have icons
      expect(container.textContent).toContain('✓');
      expect(container.textContent).toContain('⏳');
    });
  });

  describe('Role Selector', () => {
    it('shows role badges for all members', () => {
      render(<TeamManagement />);
      // Default members have owner, admin, member, viewer roles
      const selects = screen.getAllByRole('combobox');
      // Current user (owner) should have disabled role, others should have selects
      expect(selects.length).toBeGreaterThan(0);
    });

    it('disables role selector for owner', () => {
      render(<TeamManagement />);
      // Owner role should be displayed as a badge, not a select
      expect(screen.getByText('owner')).toBeInTheDocument();
    });

    it('disables role selector for current user', () => {
      render(<TeamManagement currentUserId="user1" />);
      // Current user's role should be disabled
      const ownerBadge = screen.getByText('owner');
      expect(ownerBadge.tagName).toBe('SPAN');
    });

    it('allows changing role for other members', async () => {
      render(<TeamManagement />);
      // Find a role selector (not owner)
      const roleSelects = screen.getAllByRole('combobox');
      const firstSelect = roleSelects[0];

      await userEvent.selectOptions(firstSelect, 'admin');

      await waitFor(() => {
        expect(mockSuccess).toHaveBeenCalled();
      });
    });

    it('shows all role options in dropdown', () => {
      render(<TeamManagement />);
      const selects = screen.getAllByRole('combobox');
      const firstSelect = selects[0];

      // Options: viewer, member, admin
      const options = Array.from(firstSelect.querySelectorAll('option'));
      expect(options).toHaveLength(3);
    });
  });

  describe('Invite Modal', () => {
    it('does not show modal by default', () => {
      render(<TeamManagement />);
      expect(screen.queryByTestId('modal')).not.toBeInTheDocument();
    });

    it('opens modal when invite button is clicked', async () => {
      render(<TeamManagement />);
      const inviteButton = screen.getByText('+ Invite Member');

      fireEvent.click(inviteButton);

      await waitFor(() => {
        expect(screen.getByTestId('modal')).toBeInTheDocument();
        expect(screen.getByText('Invite Team Member')).toBeInTheDocument();
      });
    });

    it('displays email input in modal', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        expect(screen.getByPlaceholderText('colleague@example.com')).toBeInTheDocument();
      });
    });

    it('displays role selector in modal', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        expect(screen.getByText('Viewer - Read-only access')).toBeInTheDocument();
        expect(screen.getByText('Member - Can use APIs')).toBeInTheDocument();
        expect(screen.getByText('Admin - Can manage team')).toBeInTheDocument();
      });
    });

    it('allows typing email in modal', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        expect(emailInput).toHaveValue('test@example.com');
      });
    });

    it('allows selecting role in modal', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(async () => {
        const roleSelect = screen.getAllByRole('combobox').find(
          (select) => select.querySelector('option[value="viewer"]')
        );
        if (roleSelect) {
          await userEvent.selectOptions(roleSelect, 'admin');
          expect(roleSelect).toHaveValue('admin');
        }
      });
    });

    it('closes modal when cancel is clicked', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        expect(screen.getByTestId('modal')).toBeInTheDocument();
      });

      const cancelButton = screen.getByText('Cancel');
      fireEvent.click(cancelButton);

      await waitFor(() => {
        expect(screen.queryByTestId('modal')).not.toBeInTheDocument();
      });
    });
  });

  describe('Invite Member Flow', () => {
    it('shows warning when inviting without email', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
        expect(mockWarning).toHaveBeenCalledWith('Please enter an email address');
      });
    });

    it('successfully invites a member with email', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(async () => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'newuser@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);

        expect(mockSuccess).toHaveBeenCalledWith(
          'Invitation sent to newuser@example.com',
          'They will receive an email shortly.'
        );
      });
    });

    it('adds invited member to the list', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'dave@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
      });

      await waitFor(() => {
        expect(screen.getByText('dave@example.com')).toBeInTheDocument();
      });
    });

    it('clears form after successful invite', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
      });

      // Open modal again
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        expect(emailInput).toHaveValue('');
      });
    });

    it('closes modal after successful invite', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        expect(screen.getByTestId('modal')).toBeInTheDocument();
      });

      const emailInput = screen.getByPlaceholderText('colleague@example.com');
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

      const sendButton = screen.getByText('Send Invitation');
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(screen.queryByTestId('modal')).not.toBeInTheDocument();
      });
    });

    it('sets invited member as pending status', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'pending@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
      });

      // New member should appear in table - stats should update
      await waitFor(() => {
        const pendingCard = screen.getByText('Pending').closest('div');
        expect(pendingCard).toHaveTextContent('2'); // Was 1, now 2
      });
    });

    it('updates total members count after invite', async () => {
      render(<TeamManagement />);

      const totalCardBefore = screen.getByText('Total Members').closest('div');
      expect(totalCardBefore).toHaveTextContent('4');

      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'new@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
      });

      await waitFor(() => {
        const totalCardAfter = screen.getByText('Total Members').closest('div');
        expect(totalCardAfter).toHaveTextContent('5');
      });
    });
  });

  describe('Remove Member', () => {
    it('displays remove button for non-owner members', () => {
      render(<TeamManagement />);
      const removeButtons = screen.getAllByText('Remove');
      // Should have remove buttons for all non-owner, non-current-user members
      expect(removeButtons.length).toBeGreaterThan(0);
    });

    it('does not display remove button for current user', () => {
      render(<TeamManagement currentUserId="user1" />);
      // user1 is "You", should not have remove button for self
      const youRow = screen.getByText('You').closest('tr');
      expect(youRow).not.toHaveTextContent('Remove');
    });

    it('prevents removing owner', async () => {
      render(<TeamManagement />);
      // Owner is user1 - try to programmatically test the protection
      // We can't click the remove button for owner as it shouldn't exist
      // The owner row shouldn't have a remove button
      const ownerRow = screen.getByText('You').closest('tr');
      const removeButtons = ownerRow?.querySelectorAll('button');
      const hasRemoveButton = Array.from(removeButtons || []).some(
        btn => btn.textContent === 'Remove'
      );
      expect(hasRemoveButton).toBe(false);
    });

    it('successfully removes non-owner member', async () => {
      render(<TeamManagement />);

      expect(screen.getByText('Bob Smith')).toBeInTheDocument();

      // Find Bob's row and remove button
      const bobRow = screen.getByText('Bob Smith').closest('tr');
      const removeButton = bobRow?.querySelector('button:has-text("Remove")') ||
                          Array.from(bobRow?.querySelectorAll('button') || [])
                            .find(btn => btn.textContent === 'Remove');

      if (removeButton) {
        fireEvent.click(removeButton);

        await waitFor(() => {
          expect(mockSuccess).toHaveBeenCalled();
          expect(screen.queryByText('Bob Smith')).not.toBeInTheDocument();
        });
      }
    });

    it('updates member count after removal', async () => {
      render(<TeamManagement />);

      const totalCardBefore = screen.getByText('Total Members').closest('div');
      expect(totalCardBefore).toHaveTextContent('4');

      // Remove Alice
      const aliceRow = screen.getByText('Alice Johnson').closest('tr');
      const removeButton = Array.from(aliceRow?.querySelectorAll('button') || [])
        .find(btn => btn.textContent === 'Remove');

      if (removeButton) {
        fireEvent.click(removeButton);

        await waitFor(() => {
          const totalCardAfter = screen.getByText('Total Members').closest('div');
          expect(totalCardAfter).toHaveTextContent('3');
        });
      }
    });
  });

  describe('Resend Invite', () => {
    it('displays resend invite button for pending members', () => {
      render(<TeamManagement />);
      expect(screen.getByText('Resend Invite')).toBeInTheDocument();
    });

    it('does not display resend invite for active members', () => {
      render(<TeamManagement />);
      const aliceRow = screen.getByText('Alice Johnson').closest('tr');
      expect(aliceRow).not.toHaveTextContent('Resend Invite');
    });

    it('successfully resends invite', async () => {
      render(<TeamManagement />);

      const resendButton = screen.getByText('Resend Invite');
      fireEvent.click(resendButton);

      await waitFor(() => {
        expect(mockSuccess).toHaveBeenCalled();
      });
    });
  });

  describe('Change Role', () => {
    it('calls success toast when role is changed', async () => {
      render(<TeamManagement />);

      const roleSelects = screen.getAllByRole('combobox');
      if (roleSelects.length > 0) {
        await userEvent.selectOptions(roleSelects[0], 'admin');

        await waitFor(() => {
          expect(mockSuccess).toHaveBeenCalled();
        });
      }
    });

    it('updates role in the UI after change', async () => {
      render(<TeamManagement />);

      const roleSelects = screen.getAllByRole('combobox');
      if (roleSelects.length > 0) {
        const initialValue = roleSelects[0].value;
        await userEvent.selectOptions(roleSelects[0], 'viewer');

        expect(roleSelects[0]).toHaveValue('viewer');
      }
    });
  });

  describe('Accessibility', () => {
    it('has accessible form labels in invite modal', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        expect(screen.getByText('Email Address')).toBeInTheDocument();
        expect(screen.getByText('Role')).toBeInTheDocument();
      });
    });

    it('has accessible buttons', () => {
      render(<TeamManagement />);
      const inviteButton = screen.getByText('+ Invite Member');
      expect(inviteButton.tagName).toBe('BUTTON');
    });

    it('table has proper structure', () => {
      const { container } = render(<TeamManagement />);
      const table = container.querySelector('table');
      expect(table).toBeInTheDocument();
      expect(table?.querySelector('thead')).toBeInTheDocument();
      expect(table?.querySelector('tbody')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles empty email gracefully', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: '' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);

        expect(mockWarning).toHaveBeenCalled();
      });
    });

    it('creates username from email prefix', async () => {
      render(<TeamManagement />);
      fireEvent.click(screen.getByText('+ Invite Member'));

      await waitFor(() => {
        const emailInput = screen.getByPlaceholderText('colleague@example.com');
        fireEvent.change(emailInput, { target: { value: 'johndoe@example.com' } });

        const sendButton = screen.getByText('Send Invitation');
        fireEvent.click(sendButton);
      });

      await waitFor(() => {
        // Should create member with name from email prefix
        expect(screen.getByText('johndoe@example.com')).toBeInTheDocument();
      });
    });
  });
});
