import { defineConfig } from '@docusaurus/types';

export default defineConfig({
  title: 'AI Book',
  tagline: 'Physical AI & Humanoid Robotics',
  url: 'https://your-vercel-site.vercel.app',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'YourOrg', // Usually GitHub org/user
  projectName: 'AI_BOOK', // Usually repo name
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          path: 'docs',
          routeBasePath: '/', // Serve docs at site root
          sidebarPath: require.resolve('./sidebars.ts'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
});