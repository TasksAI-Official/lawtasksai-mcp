#!/usr/bin/env python3
"""Generate build-release.yml with all 30 verticals."""
from pathlib import Path

verticals = [
    ("law","LawTasksAI","lawtasksai","LAWTASKSAI_LICENSE_KEY","lt_","hello@lawtasksai.com","lawtasksai.com","LawTasksAI","lawtasksai-server"),
    ("realtor","RealtorTasksAI","realtortasksai","REALTORTASKSAI_LICENSE_KEY","rt_","hello@realtortasksai.com","realtortasksai.com","RealtorTasksAI","realtortasksai-server"),
    ("farmer","FarmerTasksAI","farmertasksai","FARMERTASKSAI_LICENSE_KEY","ft_","hello@farmertasksai.com","farmertasksai.com","FarmerTasksAI","farmertasksai-server"),
    ("teacher","TeacherTasksAI","teachertasksai","TEACHERTASKSAI_LICENSE_KEY","tt_","hello@teachertasksai.com","teachertasksai.com","TeacherTasksAI","teachertasksai-server"),
    ("therapist","TherapistTasksAI","therapisttasksai","THERAPISTTASKSAI_LICENSE_KEY","th_","hello@therapisttasksai.com","therapisttasksai.com","TherapistTasksAI","therapisttasksai-server"),
    ("marketing","MarketingTasksAI","marketingtasksai","MARKETINGTASKSAI_LICENSE_KEY","mt_","hello@marketingtasksai.com","marketingtasksai.com","MarketingTasksAI","marketingtasksai-server"),
    ("contractor","ContractorTasksAI","contractortasksai","CONTRACTORTASKSAI_LICENSE_KEY","ct_","hello@contractortasksai.com","contractortasksai.com","ContractorTasksAI","contractortasksai-server"),
    ("accounting","AccountingTasksAI","accountingtasksai","ACCOUNTINGTASKSAI_LICENSE_KEY","at_","hello@accountingtasksai.com","accountingtasksai.com","AccountingTasksAI","accountingtasksai-server"),
    ("chiropractor","ChiropractorTasksAI","chiropractortasksai","CHIROPRACTORTASKSAI_LICENSE_KEY","ch_","hello@chiropractortasksai.com","chiropractortasksai.com","ChiropractorTasksAI","chiropractortasksai-server"),
    ("church","ChurchTasksAI","churchtasksai","CHURCHTASKSAI_LICENSE_KEY","cu_","hello@churchtasksai.com","churchadmintasksai.com","ChurchTasksAI","churchtasksai-server"),
    ("dentist","DentistTasksAI","dentisttasksai","DENTISTTASKSAI_LICENSE_KEY","dt_","hello@dentisttasksai.com","dentisttasksai.com","DentistTasksAI","dentisttasksai-server"),
    ("designer","DesignerTasksAI","designertasksai","DESIGNERTASKSAI_LICENSE_KEY","ds_","hello@designertasksai.com","designertasksai.com","DesignerTasksAI","designertasksai-server"),
    ("electrician","ElectricianTasksAI","electriciantasksai","ELECTRICIANTASKSAI_LICENSE_KEY","el_","hello@electriciantasksai.com","electriciantasksai.com","ElectricianTasksAI","electriciantasksai-server"),
    ("eventplanner","EventPlannerTasksAI","eventplannertasksai","EVENTPLANNERTASKSAI_LICENSE_KEY","ep_","hello@eventplannertasksai.com","eventplannertasksai.com","EventPlannerTasksAI","eventplannertasksai-server"),
    ("funeral","FuneralTasksAI","funeraltasksai","FUNERALTASKSAI_LICENSE_KEY","fu_","hello@funeraltasksai.com","funeraltasksai.com","FuneralTasksAI","funeraltasksai-server"),
    ("hr","HRTasksAI","hrtasksai","HRTASKSAI_LICENSE_KEY","hr_","hello@hrtasksai.com","hrtasksai.com","HRTasksAI","hrtasksai-server"),
    ("insurance","InsuranceTasksAI","insurancetasksai","INSURANCETASKSAI_LICENSE_KEY","in_","hello@insurancetasksai.com","insurancetasksai.com","InsuranceTasksAI","insurancetasksai-server"),
    ("landlord","LandlordTasksAI","landlordtasksai","LANDLORDTASKSAI_LICENSE_KEY","ll_","hello@landlordtasksai.com","landlordtasksai.com","LandlordTasksAI","landlordtasksai-server"),
    ("militaryspouse","MilitarySpouseTasksAI","militaryspousetasksai","MILITARYSPOUSETASKSAI_LICENSE_KEY","ms_","hello@militaryspousetasksai.com","militaryspousetasksai.com","MilitarySpouseTasksAI","militaryspousetasksai-server"),
    ("mortgage","MortgageTasksAI","mortgagetasksai","MORTGAGETASKSAI_LICENSE_KEY","mo_","hello@mortgagetasksai.com","mortgagetasksai.com","MortgageTasksAI","mortgagetasksai-server"),
    ("mortuary","MortuaryTasksAI","mortuarytasksai","MORTUARYTASKSAI_LICENSE_KEY","mu_","hello@mortuarytasksai.com","mortuarytasksai.com","MortuaryTasksAI","mortuarytasksai-server"),
    ("nutritionist","NutritionistTasksAI","nutritionisttasksai","NUTRITIONISTTASKSAI_LICENSE_KEY","nt_","hello@nutritionisttasksai.com","nutritionisttasksai.com","NutritionistTasksAI","nutritionisttasksai-server"),
    ("pastor","PastorTasksAI","pastortasksai","PASTORTASKSAI_LICENSE_KEY","pt_","hello@pastortasksai.com","pastortasksai.com","PastorTasksAI","pastortasksai-server"),
    ("personaltrainer","PersonalTrainerTasksAI","personaltrainertasksai","PERSONALTRAINERTASKSAI_LICENSE_KEY","pp_","hello@personaltrainertasksai.com","personaltrainertasksai.com","PersonalTrainerTasksAI","personaltrainertasksai-server"),
    ("plumber","PlumberTasksAI","plumbertasksai","PLUMBERTASKSAI_LICENSE_KEY","pl_","hello@plumbertasksai.com","plumbertasksai.com","PlumberTasksAI","plumbertasksai-server"),
    ("principal","PrincipalTasksAI","principaltasksai","PRINCIPALTASKSAI_LICENSE_KEY","pr_","hello@principaltasksai.com","principaltasksai.com","PrincipalTasksAI","principaltasksai-server"),
    ("restaurant","RestaurantTasksAI","restauranttasksai","RESTAURANTTASKSAI_LICENSE_KEY","re_","hello@restauranttasksai.com","restauranttasksai.com","RestaurantTasksAI","restauranttasksai-server"),
    ("salon","SalonTasksAI","salontasksai","SALONTASKSAI_LICENSE_KEY","sl_","hello@salontasksai.com","salontasksai.com","SalonTasksAI","salontasksai-server"),
    ("travelagent","TravelAgentTasksAI","travelagenttasksai","TRAVELAGENTTASKSAI_LICENSE_KEY","ta_","hello@travelagenttasksai.com","travelagenttasksai.com","TravelAgentTasksAI","travelagenttasksai-server"),
    ("vet","VetTasksAI","vettasksai","VETTASKSAI_LICENSE_KEY","vt_","hello@vettasksai.com","vettasksai.com","VetTasksAI","vettasksai-server"),
]

fields = ["product_id","product_name","mcp_key","env_var","lic_prefix","support_email","domain","app_folder","server_bin"]

def matrix_entries():
    lines = []
    for v in verticals:
        lines.append(f"          - product_id: {v[0]}")
        lines.append(f"            product_name: {v[1]}")
        lines.append(f"            mcp_key: {v[2]}")
        lines.append(f"            env_var: {v[3]}")
        lines.append(f'            lic_prefix: "{v[4]}"')
        lines.append(f"            support_email: {v[5]}")
        lines.append(f"            domain: {v[6]}")
        lines.append(f"            app_folder: {v[7]}")
        lines.append(f"            server_bin: {v[8]}")
        lines.append("")
    return "\n".join(lines)

m = matrix_entries()

yml = f"""name: Build & Release Installers

on:
  push:
    tags:
      - 'v*'

env:
  PYTHON_VERSION: '3.11'

jobs:
  build-windows:
    runs-on: windows-latest
    strategy:
      matrix:
        include:
{m}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{{{ env.PYTHON_VERSION }}}}
      - name: Install dependencies
        run: pip install pyinstaller -r requirements.txt
      - name: Build server binary
        env:
          TASKSAI_PRODUCT_ID:     ${{{{ matrix.product_id }}}}
          TASKSAI_PRODUCT_NAME:   ${{{{ matrix.product_name }}}}
          TASKSAI_MCP_KEY:        ${{{{ matrix.mcp_key }}}}
          TASKSAI_ENV_VAR:        ${{{{ matrix.env_var }}}}
          TASKSAI_LIC_PREFIX:     ${{{{ matrix.lic_prefix }}}}
          TASKSAI_SUPPORT_EMAIL:  ${{{{ matrix.support_email }}}}
          TASKSAI_DOMAIN:         ${{{{ matrix.domain }}}}
          TASKSAI_APP_FOLDER:     ${{{{ matrix.app_folder }}}}
          TASKSAI_SERVER_BIN:     ${{{{ matrix.server_bin }}}}
        run: |
          pyinstaller --onefile --name ${{{{ matrix.server_bin }}}} server.py
      - name: Write build config
        shell: python
        run: |
          with open('_build_config.py', 'w') as f:
              f.write('PRODUCT_ID = "${{{{ matrix.product_id }}}}"\\n')
              f.write('PRODUCT_NAME = "${{{{ matrix.product_name }}}}"\\n')
              f.write('MCP_KEY_NAME = "${{{{ matrix.mcp_key }}}}"\\n')
              f.write('ENV_VAR_NAME = "${{{{ matrix.env_var }}}}"\\n')
              f.write('LICENSE_PREFIX = "${{{{ matrix.lic_prefix }}}}"\\n')
              f.write('SUPPORT_EMAIL = "${{{{ matrix.support_email }}}}"\\n')
              f.write('DOMAIN = "${{{{ matrix.domain }}}}"\\n')
              f.write('APP_FOLDER = "${{{{ matrix.app_folder }}}}"\\n')
              f.write('SERVER_BIN = "${{{{ matrix.server_bin }}}}"\\n')
      - name: Build installer
        run: |
          pyinstaller --onefile `
            --add-binary "dist/${{{{ matrix.server_bin }}}}.exe;." `
            --hidden-import _build_config `
            --name "${{{{ matrix.product_name }}}}-Setup" `
            install_gui.py
      - uses: actions/upload-artifact@v4
        with:
          name: windows-${{{{ matrix.product_id }}}}
          path: dist/${{{{ matrix.product_name }}}}-Setup.exe

  build-mac:
    runs-on: macos-latest
    strategy:
      matrix:
        include:
{m}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{{{ env.PYTHON_VERSION }}}}
      - name: Install dependencies
        run: pip install pyinstaller -r requirements.txt
      - name: Build server binary
        env:
          TASKSAI_PRODUCT_ID:     ${{{{ matrix.product_id }}}}
          TASKSAI_PRODUCT_NAME:   ${{{{ matrix.product_name }}}}
          TASKSAI_MCP_KEY:        ${{{{ matrix.mcp_key }}}}
          TASKSAI_ENV_VAR:        ${{{{ matrix.env_var }}}}
          TASKSAI_LIC_PREFIX:     ${{{{ matrix.lic_prefix }}}}
          TASKSAI_SUPPORT_EMAIL:  ${{{{ matrix.support_email }}}}
          TASKSAI_DOMAIN:         ${{{{ matrix.domain }}}}
          TASKSAI_APP_FOLDER:     ${{{{ matrix.app_folder }}}}
          TASKSAI_SERVER_BIN:     ${{{{ matrix.server_bin }}}}
        run: |
          pyinstaller --onefile --name ${{{{ matrix.server_bin }}}} server.py
      - name: Write build config
        shell: python
        run: |
          with open('_build_config.py', 'w') as f:
              f.write('PRODUCT_ID = "${{{{ matrix.product_id }}}}"\\n')
              f.write('PRODUCT_NAME = "${{{{ matrix.product_name }}}}"\\n')
              f.write('MCP_KEY_NAME = "${{{{ matrix.mcp_key }}}}"\\n')
              f.write('ENV_VAR_NAME = "${{{{ matrix.env_var }}}}"\\n')
              f.write('LICENSE_PREFIX = "${{{{ matrix.lic_prefix }}}}"\\n')
              f.write('SUPPORT_EMAIL = "${{{{ matrix.support_email }}}}"\\n')
              f.write('DOMAIN = "${{{{ matrix.domain }}}}"\\n')
              f.write('APP_FOLDER = "${{{{ matrix.app_folder }}}}"\\n')
              f.write('SERVER_BIN = "${{{{ matrix.server_bin }}}}"\\n')
      - name: Build installer
        run: |
          pyinstaller --onefile \\
            --add-binary "dist/${{{{ matrix.server_bin }}}}:." \\
            --hidden-import _build_config \\
            --name "${{{{ matrix.product_name }}}}-Setup" \\
            install_gui.py
      - uses: actions/upload-artifact@v4
        with:
          name: mac-${{{{ matrix.product_id }}}}
          path: dist/${{{{ matrix.product_name }}}}-Setup

  release:
    needs: [build-windows, build-mac]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: artifacts/
      - name: List built files
        run: find artifacts/ -type f | sort
      - uses: softprops/action-gh-release@v2
        with:
          files: artifacts/**/*
          generate_release_notes: true
"""

out = Path(__file__).parent / "build-release.yml"
out.write_text(yml, encoding="utf-8")
print(f"Wrote {out} ({len(verticals)} verticals, {len(yml)} bytes)")
