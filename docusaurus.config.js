// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Comprehensive 13-Week Course for Industry Practitioners',
  favicon: 'img/favicon.ico',

  // Updated deployment URL (Vercel)
  url: 'https://vercel.com/shabanas-projects-fc5ed0bb/',
  baseUrl: '/',

  organizationName: 'Shabanabasra',
  projectName: 'AI_BOOK',

  onBrokenLinks: 'throw',
  markdown: {
    format: 'mdx',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/Shabanabasra/AI_BOOK/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/tags/**'],
          filename: 'sitemap.xml',
        },
      }),
    ],
  ],

  themeConfig:
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/Shabanabasra/AI_BOOK',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Setup Guides',
                to: '/docs/setup/workstation',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Glossary',
                to: '/docs/references/glossary',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Shabanabasra/AI_BOOK',
              },
              {
                label: 'Project Constitution',
                href: 'https://github.com/Shabanabasra/AI_BOOK/blob/main/.specify/memory/constitution.md',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml'],
      },
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      algolia: {
        appId: 'YOUR_APP_ID',
        apiKey: 'YOUR_SEARCH_API_KEY',
        indexName: 'physical-ai-textbook',
        contextualSearch: true,
        searchParameters: {
          attributesToRetrieve: [
            'hierarchy',
            'content',
            'url',
            'week',
            'module',
            'capstone_component',
          ],
        },
        searchPagePath: 'search',
      },
      metadata: [
        {name: 'keywords', content: 'robotics, physical AI, humanoid robots, ROS 2, Isaac Sim, VLA'},
        {name: 'description', content: 'Comprehensive 13-week textbook for industry practitioners learning Physical AI and Humanoid Robotics'},
        {property: 'og:title', content: 'Physical AI & Humanoid Robotics Textbook'},
        {property: 'og:description', content: 'Master Physical AI, ROS 2, Digital Twins, and Humanoid Robotics in 13 weeks'},
        {property: 'og:type', content: 'website'},
      ],
    }),
};

export default config;