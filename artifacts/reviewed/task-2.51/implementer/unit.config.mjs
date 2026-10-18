export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartLegendPanel.test.tsx"], maxWorkers: 1, fileParallelism: false },
};
