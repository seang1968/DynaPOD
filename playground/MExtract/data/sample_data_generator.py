import pandas as pd

columns = [
    "GuestAppId_Key", "Region", "ESX_Guest", "ESX_Host", "Cluster_Name", "VCenter", 
    "Virtual_Processors", "Total_Mem (MB)", "#Samples", "Avg_Phys_CPU", "Max_Phys_CPU", 
    "P95(Phys_CPU)", "P90(Phys_CPU)", "Avg_Virt_CPU", "Max_Virt_CPU", "P95(Virt_CPU)", 
    "P90(Virt_CPU)", "Avg_Mem_Util", "Max_Mem_Util", "P95(Mem_Util)", "P90(Mem_Util)", 
    "Avg_virCPU_Ready", "Max_virCPU_Ready", "P95(virCPU_Ready)", "P90(virCPU_Ready)", 
    "Avg_Balloon_Mem", "Max_Balloon_Mem", "P95(Balloon_Mem)", "P90(Balloon_Mem)", 
    "Avg_Mem", "Max_Mem_Consumed (%)", "P95(Mem_Consumed %)", "P90(Mem_Consumed %)", 
    "Avg_Net_Rate (MB/s)", "Max_Net_Rate (MB/s)", "P95(Net_Rate)", "P90(Net_Rate)", 
    "TIO_Avg (MB/s)", "TIO_Max (MB/s)", "TIO_P95 (MB/s)", "TIO_P90 (MB/s)", 
    "Avg_Disk_Phys_IO_Rate (R/s)", "Max_Disk_Phys_IO", "Function_Type", 
    "Business_Criticality", "Is_Risk", "Development_Model", "Hosting_Model", 
    "Data_Ownership", "Ownership_Model", "Operating_Environment", "SOX_Indicator", 
    "High_Financial_Risk", "Information_Classification", "First_Date", "Idle", 
    "Recommended_CPU", "Recommended_MEM"  # Correct last column CI
]

def generate_csv(columns, num_rows=100):
    data = {col: [f"SampleData_{i}" for i in range(num_rows)] for col in columns}
    df = pd.DataFrame(data)
    df.to_csv("Monthly_ESX_GUEST_REPORT_v2_JUL_2024.csv", index=False)

if __name__ == "__main__":
    generate_csv(columns)
