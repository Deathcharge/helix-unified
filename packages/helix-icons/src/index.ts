/**
 * @helix/icons - Custom Helix Icon Set
 * Replaces lucide-react with brand-specific icons
 */

import React from 'react';

export interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number | string;
  color?: string;
  strokeWidth?: number;
}

const createIcon = (
  displayName: string,
  path: string | string[]
): React.FC<IconProps> => {
  const Icon: React.FC<IconProps> = ({
    size = 24,
    color = 'currentColor',
    strokeWidth = 2,
    ...props
  }) => {
    const paths = Array.isArray(path) ? path : [path];

    return React.createElement(
      'svg',
      {
        width: size,
        height: size,
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: color,
        strokeWidth,
        strokeLinecap: 'round' as const,
        strokeLinejoin: 'round' as const,
        ...props,
      },
      ...paths.map((d, i) =>
        React.createElement('path', { key: i, d })
      )
    );
  };

  Icon.displayName = displayName;
  return Icon;
};

// Core Helix Icons
export const HelixLogo = createIcon(
  'HelixLogo',
  [
    'M12 2L2 7v10l10 5 10-5V7z',
    'M12 22v-5',
    'M2 7l10 5 10-5',
    'M7 9.5v5l5 2.5 5-2.5v-5'
  ]
);

export const HelixSpin = createIcon(
  'HelixSpin',
  [
    'M12 2a10 10 0 0 1 10 10',
    'M12 2a10 10 0 0 0-10 10',
    'M12 22a10 10 0 0 0 10-10',
    'M12 22a10 10 0 0 1-10-10'
  ]
);

// Navigation Icons
export const Dashboard = createIcon(
  'Dashboard',
  'M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z'
);

export const Menu = createIcon(
  'Menu',
  ['M3 12h18', 'M3 6h18', 'M3 18h18']
);

export const Close = createIcon(
  'Close',
  ['M18 6L6 18', 'M6 6l12 12']
);

export const ChevronLeft = createIcon(
  'ChevronLeft',
  'M15 18l-6-6 6-6'
);

export const ChevronRight = createIcon(
  'ChevronRight',
  'M9 18l6-6-6-6'
);

export const ChevronDown = createIcon(
  'ChevronDown',
  'M6 9l6 6 6-6'
);

export const ChevronUp = createIcon(
  'ChevronUp',
  'M18 15l-6-6-6 6'
);

// Action Icons
export const Plus = createIcon(
  'Plus',
  ['M12 5v14', 'M5 12h14']
);

export const Minus = createIcon(
  'Minus',
  'M5 12h14'
);

export const Edit = createIcon(
  'Edit',
  ['M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7', 'M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z']
);

export const Trash = createIcon(
  'Trash',
  ['M3 6h18', 'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2']
);

export const Copy = createIcon(
  'Copy',
  ['M20 9h-9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2z', 'M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1']
);

export const Download = createIcon(
  'Download',
  ['M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4', 'M7 10l5 5 5-5', 'M12 15V3']
);

export const Upload = createIcon(
  'Upload',
  ['M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4', 'M17 8l-5-5-5 5', 'M12 3v12']
);

export const Search = createIcon(
  'Search',
  ['M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z', 'M21 21l-4.35-4.35']
);

export const Filter = createIcon(
  'Filter',
  'M22 3H2l8 9.46V19l4 2v-8.54L22 3z'
);

export const Settings = createIcon(
  'Settings',
  ['M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z', 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z']
);

// Status Icons
export const Check = createIcon(
  'Check',
  'M20 6L9 17l-5-5'
);

export const AlertCircle = createIcon(
  'AlertCircle',
  ['M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z', 'M12 8v4', 'M12 16h.01']
);

export const Info = createIcon(
  'Info',
  ['M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z', 'M12 16v-4', 'M12 8h.01']
);

export const Warning = createIcon(
  'Warning',
  ['M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z', 'M12 9v4', 'M12 17h.01']
);

export const Error = createIcon(
  'Error',
  ['M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z', 'M15 9l-6 6', 'M9 9l6 6']
);

export const Success = createIcon(
  'Success',
  ['M22 11.08V12a10 10 0 1 1-5.93-9.14', 'M22 4L12 14.01l-3-3']
);

// User Icons
export const User = createIcon(
  'User',
  ['M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2', 'M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z']
);

export const Users = createIcon(
  'Users',
  ['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2', 'M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z', 'M23 21v-2a4 4 0 0 0-3-3.87', 'M16 3.13a4 4 0 0 1 0 7.75']
);

export const UserPlus = createIcon(
  'UserPlus',
  ['M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2', 'M8.5 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z', 'M20 8v6', 'M23 11h-6']
);

// Communication Icons
export const Mail = createIcon(
  'Mail',
  ['M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z', 'M22 6l-10 7L2 6']
);

export const MessageCircle = createIcon(
  'MessageCircle',
  ['M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z']
);

export const Bell = createIcon(
  'Bell',
  ['M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9z', 'M13.73 21a2 2 0 0 1-3.46 0']
);

// File Icons
export const File = createIcon(
  'File',
  ['M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z', 'M13 2v7h7']
);

export const FileText = createIcon(
  'FileText',
  ['M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z', 'M14 2v6h6', 'M16 13H8', 'M16 17H8', 'M10 9H8']
);

export const Folder = createIcon(
  'Folder',
  'M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'
);

export const FolderOpen = createIcon(
  'FolderOpen',
  ['M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z', 'M2 10h20']
);

// Agent-Specific Icons
export const Agent = createIcon(
  'Agent',
  ['M12 2L2 7l10 5 10-5-10-5z', 'M2 17l10 5 10-5', 'M2 12l10 5 10-5']
);

export const Brain = createIcon(
  'Brain',
  ['M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2zM14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2z']
);

export const Consciousness = createIcon(
  'Consciousness',
  ['M12 2L2 7v10l10 5 10-5V7z', 'M12 2v20', 'M2 7l10 5 10-5', 'M7 9.5l5 2.5 5-2.5', 'M7 14.5l5 2.5 5-2.5']
);

export const Network = createIcon(
  'Network',
  ['M12 2v20', 'M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6']
);

// Export all icons as default
export default {
  HelixLogo,
  HelixSpin,
  Dashboard,
  Menu,
  Close,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Plus,
  Minus,
  Edit,
  Trash,
  Copy,
  Download,
  Upload,
  Search,
  Filter,
  Settings,
  Check,
  AlertCircle,
  Info,
  Warning,
  Error,
  Success,
  User,
  Users,
  UserPlus,
  Mail,
  MessageCircle,
  Bell,
  File,
  FileText,
  Folder,
  FolderOpen,
  Agent,
  Brain,
  Consciousness,
  Network,
};
