export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartTypeGallery.test.tsx"], maxWorkers: 1, fileParallelism: false },
};
