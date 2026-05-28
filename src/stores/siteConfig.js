import { defineStore } from 'pinia'
import { defaultSiteConfig } from '@/data/defaultConfig'
import { defaultPages } from '@/data/defaultPages'
import { getSiteConfig, getPage } from '@/services/api'

export const useSiteConfigStore = defineStore('siteConfig', {
  state: () => ({
    config: { ...defaultSiteConfig },
    pages: { ...defaultPages },
    loaded: false,
  }),
  getters: {
    hero: (state) => state.config.hero,
    about: (state) => state.config.about,
    members: (state) => state.config.members,
    products: (state) => state.config.products,
    openSource: (state) => state.config.openSource,
    footer: (state) => state.config.footer,
    sections: (state) => state.config.sections || {},
    getPage: (state) => (slug) => state.pages[slug] || null,
  },
  actions: {
    async init() {
      this.config = { ...defaultSiteConfig }
      this.pages = { ...defaultPages }
      this.loaded = true

      try {
        const remoteConfig = await getSiteConfig()
        if (remoteConfig) {
          this.config = { ...defaultSiteConfig, ...remoteConfig }
        }

        const slugs = Object.keys(defaultPages)
        const results = await Promise.allSettled(slugs.map((slug) => getPage(slug)))
        results.forEach((result, i) => {
          if (result.status === 'fulfilled' && result.value) {
            const defaultPage = defaultPages[slugs[i]]
            if (defaultPage) {
              this.pages[slugs[i]] = {
                ...result.value,
                content: { ...defaultPage.content, ...result.value.content },
              }
            } else {
              this.pages[slugs[i]] = result.value
            }
          }
        })
      } catch (e) {
        console.warn('API 不可用，使用本地默认数据', e)
      }
    },
  },
})
