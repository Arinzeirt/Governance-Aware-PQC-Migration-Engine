from components.v1_topbar import show as show_topbar
from components.v1_navigation import show as show_navigation
from components.v1_executive_overview import show as show_posture
from components.v1_enterprise_kpi import show as show_kpi

from components.enterprise_scan_results import show as show_scan_results
from components.compliance_readiness import show as show_compliance
from components.executive_findings import show as show_findings
from components.executive_roadmap import show as show_roadmap


def show():

    show_topbar()

    show_navigation()

    show_posture()

    show_kpi()

    show_scan_results()

    show_compliance()

    show_findings()

    show_roadmap()

