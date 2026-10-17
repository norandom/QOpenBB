import { fireEvent, render, screen, cleanup } from "/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/node_modules/@testing-library/react";
import { expect, it, vi, afterEach } from "/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/node_modules/vitest";
import { ChartSetupPanel } from "/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/setup/ChartSetupPanel";
afterEach(cleanup);
it("ignores missing drag source when caller supplies empty stable ID", () => {
 const onEdit = vi.fn();
 render(<ChartSetupPanel value={{categoryId:"period",aggregate:false,aggregationMethod:"sum",series:[{id:"",label:"Empty ID"},{id:"b",label:"B"}],switchCategorySeries:false}} categories={[]} aggregationMethods={[]} onEdit={onEdit} />);
 fireEvent.drop(screen.getByRole("button",{name:"Reorder B"}), {dataTransfer:{dropEffect:""}});
 expect(onEdit).not.toHaveBeenCalled();
});
