#!/usr/bin/env python3
import os, subprocess

from auto_cpufreq.config.config import config
from auto_cpufreq.globals import POWER_SUPPLY_DIR

def set_battery(value, mode, bat):
    path = f"{POWER_SUPPLY_DIR}{bat}/charge_{mode}_threshold"
    if os.path.isfile(path): subprocess.check_output(f"echo {value} | tee {path}", shell=True, text=True)
    else: print(f"WARNING: {path} does NOT exist")

def get_threshold_value(mode):
    conf = config.get_config()
    return conf["battery"][f"{mode}_threshold"] if conf.has_option("battery", f"{mode}_threshold") else (0 if mode == "start" else 100)

def ideapad_acpi_setup():
    conf = config.get_config()

    if not (conf.has_option("battery", "enable_thresholds") and conf["battery"]["enable_thresholds"] == "true"): return

    if os.path.exists(POWER_SUPPLY_DIR):
        batteries = [name for name in os.listdir(POWER_SUPPLY_DIR) if name.startswith('BAT')]
        
        for bat in batteries:
            set_battery(get_threshold_value("start"), "start", bat)
            set_battery(get_threshold_value("stop"), "stop", bat)
    else: print("WARNING: could NOT access", POWER_SUPPLY_DIR)

def ideapad_acpi_print_thresholds():
    batteries = [name for name in os.listdir(POWER_SUPPLY_DIR) if name.startswith('BAT')]
    print("\n-------------------------------- Battery Info ---------------------------------\n")
    print(f"battery count = {len(batteries)}")
    for bat in batteries:
        try:
            print(f'{bat} start threshold = {subprocess.getoutput(f"cat {POWER_SUPPLY_DIR}{bat}/charge_start_threshold")}')
            print(f'{bat} start threshold = {subprocess.getoutput(f"cat {POWER_SUPPLY_DIR}{bat}/charge_stop_threshold")}')
        except Exception as e: print(f"ERROR: failed to read battery {bat} thresholds:", repr(e))
