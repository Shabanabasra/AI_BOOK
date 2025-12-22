module.exports = {
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
          path: '../docs', // Point to the docs directory in the root
          routeBasePath: '/', // Serve docs at site root
          sidebarPath: false, // Disable sidebar auto-generation for now to fix broken links
          showLastUpdateTime: false,
          showLastUpdateAuthor: false,
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/index.css'),
        },
      },
    ],
  ],
};