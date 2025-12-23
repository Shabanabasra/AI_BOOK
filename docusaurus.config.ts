module.exports = {
  title: 'AI Book',
  tagline: 'Physical AI & Humanoid Robotics',
  url: 'https://your-vercel-site.vercel.app',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'YourOrg', // GitHub org/user
  projectName: 'AI_BOOK', // Repo name
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          path: 'docs/AI_BOOK', // <-- Root folder me docs
          routeBasePath: '/',    // Serve docs at root
          sidebarPath: require.resolve('./sidebars.js'),
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