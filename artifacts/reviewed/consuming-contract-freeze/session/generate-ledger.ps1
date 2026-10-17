$ErrorActionPreference='Stop'
$out='artifacts/consuming-contract-freeze/session'
$runtime='artifacts/reviewed/parity/editor-runtime-next'
$inventory='artifacts/reviewed/parity/chart-editor-capture/control-inventory.json'
$controls=Get-Content -Raw "$runtime/control-ledger.json"|ConvertFrom-Json
$patches=Get-Content -Raw "$runtime/patch-ledger.json"|ConvertFrom-Json
$domains=Get-Content -Raw "$runtime/domains.json"|ConvertFrom-Json
$rows=[System.Collections.Generic.List[object]]::new()
function Ref($p,$pointer){ [ordered]@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant();pointer=$pointer} }
$mapping=@{
 'Horizontal Axis|Padding'='horizontal-label-padding-9';'Horizontal Axis|Auto Rotate'='horizontal-label-auto-rotate-off';
 'Vertical Axis|Size'='vertical-label-size-14';'Legend|Weight'='legend-weight-bold';'Legend|Size'='legend-size-14';
 'Legend|Marker Size'='legend-marker-size-15';'Legend|Horizontal Spacing'='legend-horizontal-spacing-40';
 'Series|Labels'='series-labels-on';'Series|Stroke Width'='series-stroke-width-3';
 'Line Series|Markers'='line-markers-on';'Line Series|Shape'='line-marker-shape';'Line Series|Size'='line-marker-size-9';
 'Set Up|Aggregate'='setup/Aggregate/on';'Set Up|Switch Category / Series'='setup/Switch Category / Series/on'
}
for($i=0;$i -lt $controls.Count;$i++){
 $record=$controls[$i];$name=$record.source
 $group=if($name -match 'line-'){ 'Line Series' }elseif($name -match 'Horizontal-Axis'){ 'Horizontal Axis' }elseif($name -match 'Vertical-Axis'){ 'Vertical Axis' }elseif($name -match 'Legend'){ 'Legend' }elseif($name -match 'Series'){ 'Series' }elseif($name -match 'setup-'){ 'Set Up' }else{ 'Initial chart' }
 for($j=0;$j -lt $record.controls.Count;$j++){
  $c=$record.controls[$j];$label=$c.label;$kind=if($c.role){$c.role}else{$c.type};$key="$group|$label"
  $action=$mapping[$key];if($group -eq 'Vertical Axis' -and $label -eq 'Thickness' -and $j -lt 3){$action='vertical-thickness-3'}
  $patch=$patches|Where-Object label -EQ $action|Select-Object -First 1
  $refs=@((Ref "$runtime/control-ledger.json" "/$i/controls/$j"),(Ref "$runtime/$name" '/ui'))
  if($patch){$refs+=Ref "$runtime/patch-ledger.json" ('/label='+$action)}
  $domain=[ordered]@{kind=$kind;observedValue=$c.value;checked=$c.checked;min=$c.min;max=$c.max;step=$c.step;complete=$false}
  if($kind -eq 'checkbox'){$domain.values=@($false,$true);$domain.complete=$true}
  $menu=$domains|Where-Object { $_.label -eq $label -and (($group -eq 'Legend' -and $_.source -match 'Legend') -or ($group -eq 'Vertical Axis' -and $_.source -match 'Vertical') -or ($label -eq 'Tooltip Mode')) }|Select-Object -First 1
  if($menu){$domain.observedMenu=$menu.options;$refs+=Ref "$runtime/domains.json" ('/source='+$menu.source)}
  $paths=@($patch.modelDelta|ForEach-Object {$_.path})
  $pred='Observed in dark groupedColumn fixture with '+$group+' expanded; exact cross-family predicate unverified.'
  if($group -eq 'Line Series'){$pred='Observed after Line transition; marker Shape/Size/Stroke Width appear after Markers on; other family conditions unverified.'}
  if($group -eq 'Set Up'){$pred='Set Up selected; Sum dropdown appears when Aggregate checked; category/series conditions unverified.'}
  $effect=if($patch){[ordered]@{action=$action;modelDelta=$patch.modelDelta;effectiveDelta=$patch.effectiveDelta;scope='Finite captured value only; no general projection/candidate acceptance.'}}else{[ordered]@{status='unresolved';reason='Control observation is not an event/effect contract.'}}
  if($label -eq 'Tooltip Mode' -and $group -eq 'Series'){
   $paths=@('chartOptions.bar.tooltip.mode');$effect=[ordered]@{single='Category and hovered Revenue 100';shared='Category, Revenue 100 and Operating Income 20';compact='Revenue 100 without category';scope='Finite groupedColumn hover only; null/ties/order/keyboard unresolved'}
   $refs+=Ref 'artifacts/reviewed/parity/editor-contract-close/event-ledger.json' '/labels=tooltip-Single,tooltip-Multiple,tooltip-Compact'
  }
  $query='At original 38dffc3 with the same synthetic fixture, select '+$(if($group -eq 'Set Up'){'Set Up'}else{'Customize'})+', expand '+$group+', target visible '+$kind+' label '+$(if($label){'"'+$label+'"'}else{'<unlabelled, identify from enclosing field and control index '+$j+'>'})+' in '+$name+'; capture exact label/ancestor, conditional visibility, menu domain, one edit delta, settled effect, restoration and keyboard focus in light/dark.'
  $rows.Add([ordered]@{id="runtime-$i-$j";label=$label;tab=$(if($group -eq 'Set Up'){'Set Up'}else{'Customize'});group=$group;family=$(if($group -eq 'Line Series'){'line'}else{'groupedColumn'});domain=$domain;namespace=$paths;originalPredicate=$pred;effect=$effect;references=$refs;coverage=[ordered]@{control='observed-finite';event=$(if($paths.Count){'observed-finite'}else{'unresolved'});candidate='unverified';predicate='finite-only';geometryKeyboard='unverified'};captureQuery=$query})
 }
}
$inv=Get-Content -Raw $inventory|ConvertFrom-Json
foreach($prop in $inv.PSObject.Properties){
 if($prop.Name -notin @('group-Chart-Style','group-Titles','title-enabled','title-after','chart-panel','data-panel')){continue}
 $case=$prop.Name;$list=$prop.Value.controls
 for($j=0;$j -lt $list.Count;$j++){
  $c=$list[$j];if($c.visible -ne $true){continue}
  $group=if($case -match 'Style'){'Chart Style'}elseif($case -match 'Title|title'){'Titles'}elseif($case -eq 'data-panel'){'Set Up'}else{'Chart'}
  $rows.Add([ordered]@{id="inventory-$case-$j";label=$c.label;tab=$(if($group -eq 'Chart'){'Chart'}elseif($group -eq 'Set Up'){'Set Up'}else{'Customize'});group=$group;family='groupedColumn';domain=[ordered]@{kind=$c.type;observedValue=$c.value;checked=$c.checked;complete=$false};namespace=@();originalPredicate='Computed visible in this case only. Hidden DOM siblings excluded; full conditional predicate unresolved.';effect=[ordered]@{status='unresolved';reason='No namespace inferred from repeated/unlabelled controls or panel text.'};references=@((Ref $inventory ('/'+$case+'/controls/'+$j)));coverage=[ordered]@{control='observed-finite';event='unresolved';candidate='unverified';predicate='finite-only';geometryKeyboard='unverified'};captureQuery="Reopen original $case; identify the enclosing field for visible control index $j ($($c.label)); edit independently, record exact event/model/effective leaves and compare conditional DOM/focus/geometry before/after in light/dark."})
 }
}
$accepted=@(
 @('title-text','Title','Titles','string including empty','bar.title.text','title'),
 @('title-enabled','Chart Title','Titles','boolean','bar.title.enabled','title'),
 @('legend-position','Position','Legend','top,bottom,left,right','bar.legend.position','legend'),
 @('stroke-width','Stroke Width','Series','finite number >= 0; UI range 0..10','bar.series.strokeWidth','stroke'),
 @('tooltip-mode','Tooltip Mode','Series','single,shared,compact; UI Multiple=shared','bar.tooltip.mode','tooltip')
)
foreach($a in $accepted){
 $rows.Add([ordered]@{id='supported-'+$a[0];label=$a[1];tab='Customize';group=$a[2];family=$(if($a[0] -eq 'tooltip-mode'){'groupedColumn only; exact valid stacked event unresolved'}else{'groupedColumn and stackedColumn accepted mapper domain; finite UI captures distinct'});domain=$a[3];namespace=@($a[4]);originalPredicate='Preserve original group and enabled-field visibility; no capability predicate. Complete conditional UI remains unverified.';effect='Exact existing mapColumnEditorEvent/applyColumnEdit patch; no derived render writes. '+$(if($a[0] -eq 'title-enabled'){'Text retained while disabled.'}else{''});references=@((Ref 'vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/editorEvents.ts' '/mapColumnEditorEvent'),(Ref 'vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/optionStateTypes.ts' '/ColumnEditorEvent'),(Ref $(if($a[0] -eq 'tooltip-mode'){'artifacts/reviewed/parity/editor-contract-close/event-ledger.json'}else{'artifacts/reviewed/parity/editor-payload-capture/payload-deltas.json'}) $(if($a[0] -eq 'tooltip-mode'){'/labels=tooltip-Single,tooltip-Multiple,tooltip-Compact'}else{'/stage='+$a[5]})));coverage=[ordered]@{command='implemented-source-contract';control='finite-original';candidateUI='unverified';fullEditor='unverified'};captureQuery='Candidate real application: dispatch '+$a[0]+' through original docked control, inspect exact addressed save/model, visible effect, light/dark, close/reopen and backend restart/readback.'})
}
$unknown=@(
 @('Color','Chart Style / Titles / Legend / Series / Axes','Open every visible color picker, record accepted inputs, enable/disable retention, exact family/axis-position paths, opaque/alpha effect, keyboard and light/dark geometry.'),
 @('Top / Right / Bottom / Left','Chart Style','Identify each unlabelled spacing pair by enclosing field; edit one side at a time, record exact namespace and visible plot padding; repeat after family/theme/save-reopen.'),
 @('Subtitle / Horizontal Axis Title / Vertical Axis Title','Titles','Enable each independently; capture text, font, weight+style, size, color and spacing edit paths; disable/on retains text; compare title/axis geometry and formatter interaction.'),
 @('Shadow','Series','Enable Shadow and enumerate newly visible fields; edit each with independent event/model/effective/raster evidence; establish family conditions and retained disabled values.'),
 @('Grid Lines / Ticks / Axis Type / Position','Horizontal Axis / Vertical Axis','Toggle each group on/off, enumerate nested controls and menu options, edit one leaf, capture category versus number plus position-specific paths and settle original line/grid/tick effect.'),
 @('Categories / series selection and reorder','Set Up','Select a different category and reorder numeric series using original UI; record ordered range/model/row and stable-ID bindings, duplicates, deselection, mixed/unknown unit provenance and return-to-table behavior.'),
 @('Aggregate function','Set Up','Open function menu after Aggregate on; record full domain. For each admitted function capture numeric null/absent/zero/negative cases, repeated-category identity, units and restoration; finite Sum present-values is already evidence.'),
 @('Chart thumbnails','Chart','Enumerate actual thumbnails/selection labels in each family group with flags; capture destination model/range and prior-family restoration. Public enum inventory alone is not control completion.'),
 @('Close / reopen / tab / scroll / focus','External and docked','At each tab, scroll and focus a nested control, close chevron, reopen via external action; repeat theme/family switch and keyboard. Capture root chartSettingsOpen, active tab, viewport, focus and return-to-table selection/widths.'),
 @('Export / quick fills / navigator / mini-chart','External actions','Exercise original action conditions then enabled effects, original filename/menu/download format, latest data/theme pixels and backend save/reopen. Keep original no-series, multi-series and forecast predicates.'),
 @('Light / detached / forecast / other families','All','Repeat targeted known-control cases under original light mode, detached and forecast flags, and each consuming family; record conditional controls rather than extrapolating dark groupedColumn.'),
 @('Tooltip invocation','Series','For each mode capture duplicate categories, tied values, null/absent/zero/negative series, pointer hit tests and keyboard: hovered identity, entry order and omission, escaping and precision 0/3.'),
 @('Font menus and combinations','Titles / Legend / Series / Axes','Open each original font/weight/size menu independently; edit normal/bold/italic/bold italic/predefined, capture exact fontWeight/fontStyle pair and reset. Do not apply one menu domain to all groups.')
)
$ledger=[ordered]@{status='draft-input-for-controller; not-full-editor-or-activation-approval';date='2026-10-17';candidate='ea02ec15956dee8d2c8a06825387a570757db12d';original='38dffc33389aca0e4a87e0e88d42f7067aa220df';method='Read-only reuse of finite reviewed control/event projections. 295 total rows = 202 runtime capture rows + 88 inventory capture rows + 5 supported-command rows; 290 finite capture rows, not 295 independent observations. Rows preserve capture index; repeated slider/number pairs and cases are deliberate. Missing namespace is unknown, not absence.';counts=[ordered]@{totalRows=$rows.Count;runtimeCaptureRows=@($rows|Where-Object {$_.id -like 'runtime-*'}).Count;inventoryCaptureRows=@($rows|Where-Object {$_.id -like 'inventory-*'}).Count;supportedCommandRows=@($rows|Where-Object {$_.id -like 'supported-*'}).Count};rows=$rows;unresolved=@($unknown|ForEach-Object {[ordered]@{label=$_[0];tabGroup=$_[1];captureQuery=$_[2];status='unresolved'}});nonClaims=@('Not a complete field inventory.','Computed visibility is not in-viewport or keyboard geometry evidence.','Observed finite event/effective values are not candidate projections.','Outgoing POST is not backend readback/reopen/restart.','No browser/test/build/install/network execution in this lane.')}
$ledger|ConvertTo-Json -Depth 25|Set-Content -LiteralPath "$out/editor-field-ledger.json" -Encoding utf8
"rows=$($rows.Count); unknownQueries=$($unknown.Count); supportedCommands=$($accepted.Count)"

