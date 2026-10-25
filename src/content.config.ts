import { glob } from 'astro/loaders';
import { defineCollection, z } from 'astro:content';

export const collections = {
  projects: defineCollection({
    loader: glob({ pattern: '**/*.md', base: 'src/content/projects' }),
    schema: z.object({
      title: z.string(),
      description: z.string(),
      date: z.coerce.date(),
      categories: z.array(z.string()).default([]),
      tags: z.array(z.string()).default([]),
      technologies: z.array(z.string()).default([]),
      status: z.string().default('In Progress'),
    }),
  }),
  articles: defineCollection({
    loader: glob({ pattern: '**/*.md', base: 'src/content/articles' }),
    schema: z.object({
      title: z.string(),
      description: z.string(),
      date: z.coerce.date(),
      categories: z.array(z.string()).default([]),
      tags: z.array(z.string()).default([]),
    }),
  }),
};
