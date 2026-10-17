export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartTitlesPanel.test.tsx"], maxWorkers: 1, fileParallelism: false },
};

