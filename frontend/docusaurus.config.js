import { defineConfig } from 'docusaurus';

export default defineConfig({
  title: 'AI Book',
  tagline: 'Physical AI & Humanoid Robotics Textbook',
  url: 'https://your-vercel-project.vercel.app', // aapka Vercel URL
  baseUrl: '/', // site root se serve ho
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-github-org', // GitHub org/user name
  projectName: 'AI_BOOK', // repository name
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // docs root par serve hon
          sidebarPath: require.resolve('./sidebars.ts'),
          editUrl: 'https://github.com/your-org/AI_BOOK/edit/main/',
        },
        blog: false, // agar blog nahi chahiye
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
});