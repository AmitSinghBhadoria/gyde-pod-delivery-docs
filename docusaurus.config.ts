import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Gyde POD Delivery Docs',
  tagline: 'The operating system for Gyde delivery PODs',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://amitsinghbhadoria.github.io',
  baseUrl: '/gyde-pod-delivery-docs/',

  organizationName: 'AmitSinghBhadoria',
  projectName: 'gyde-pod-delivery-docs',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl:
            'https://github.com/AmitSinghBhadoria/gyde-pod-delivery-docs/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Gyde POD',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'engagementSidebar',
          position: 'left',
          label: 'Engagement Docs',
        },
        {
          href: 'https://github.com/AmitSinghBhadoria/gyde-pod-delivery-docs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Gyde AI POD Framework | Confidential`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
