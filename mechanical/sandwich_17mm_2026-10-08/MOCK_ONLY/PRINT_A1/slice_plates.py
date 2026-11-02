"""Local Bambu Studio slicing only. No network/printer calls."""
from pathlib import Path
import subprocess,json,sys,shutil,hashlib
HERE=Path(__file__).resolve().parent
result_file=HERE/'slice-results.json'
records=json.loads(result_file.read_text()) if result_file.exists() else {}
for row in json.loads((HERE/'print-plan.json').read_text())['print_plan']:
    if row['material']!='PLA':continue
    if len(sys.argv)>1 and row['plate'] not in sys.argv[1:]:continue
    out=HERE/'jobs'/row['job_id'];out.mkdir(parents=True,exist_ok=True)
    (HERE/'sliced').mkdir(exist_ok=True)
    suffix={0.2:'02',0.4:'',0.6:'06'}[row['nozzle_mm']]
    machine='printer'+suffix
    filament='PLA'+suffix
    args=['D:/Bambu Studio/bambu-studio.exe','--load-settings',str(HERE/'presets'/(machine+'.json'))+';'+str(HERE/'presets'/(row['process']+'.json')),'--load-filaments',str(HERE/'presets'/(filament+'.json')),'--curr-bed-type','Textured PEI Plate','--arrange','0','--slice','0','--debug','2','--outputdir',str(out),'--export-3mf','part.gcode.3mf',str(HERE/row['file'])]
    r=subprocess.run(args,capture_output=True,text=True)
    (out/'cli.log').write_text(r.stdout+r.stderr,encoding='utf-8')
    result=json.loads((out/'result.json').read_text()) if (out/'result.json').exists() else {}
    if result.get('return_code')==0:
        shutil.copyfile(out/'part.gcode.3mf',HERE/'sliced'/(row['plate']+'.gcode.3mf'))
        result['input_sha256']=hashlib.sha256((HERE/row['file']).read_bytes()).hexdigest()
        records[row['plate']]=result
        result_file.write_text(json.dumps(records,indent=2))
        assert out.resolve().is_relative_to((HERE/'jobs').resolve())
        shutil.rmtree(out)
    print(row['job_id'],row['plate'],r.returncode,result.get('error_string'),flush=True)
