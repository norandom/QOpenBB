export default {
  esbuild: { jsx: "automatic" },
  test: { environment: "jsdom", include: ["tests/unit/chartEditorDock.test.tsx"], maxWorkers: 1, fileParallelism: false },
};

