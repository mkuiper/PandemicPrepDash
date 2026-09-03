"""
Data Governance, Cloud Infrastructure & Compute Resources Configuration Models.
Aligns with Australian Information Security Manual (ISM) and Protective Security Policy Framework (PSPF).
"""

from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class CloudProviderType(str, Enum):
    LOCAL_GPU_CLUSTER = "local_gpu_cluster"
    AWS_HEALTHOMICS = "aws_healthomics"
    GCP_LIFE_SCIENCES = "gcp_life_sciences"
    AZURE_HPC = "azure_hpc"
    HYBRID_SOVEREIGN_CLOUD = "hybrid_sovereign_cloud"


class SecurityClassification(str, Enum):
    UNCLASSIFIED = "UNCLASSIFIED"
    OFFICIAL = "OFFICIAL"
    OFFICIAL_SENSITIVE = "OFFICIAL: SENSITIVE"
    PROTECTED = "PROTECTED"


class ComplianceFramework(BaseModel):
    pspf_aligned: bool = True
    ism_controls_verified: bool = True
    data_residency: str = "Australia (Sydney / Melbourne ap-southeast-2)"
    ssba_custodianship_audit: bool = True
    irap_cloud_tier: str = "PROTECTED Level Assessed"
    privacy_act_1988_compliant: bool = True


class CloudComputeConfig(BaseModel):
    provider: CloudProviderType = CloudProviderType.LOCAL_GPU_CLUSTER
    cluster_endpoint: str = "https://hpc.cluster.internal.gov.au/v1"
    gpu_type: str = "NVIDIA H100 (80GB SXM5)"
    gpu_count: int = 4
    max_concurrent_nodes: int = 8
    execution_timeout_seconds: int = 3600
    cloud_storage_bucket: str = "s3://aus-biosecurity-vault-ap-southeast-2/"
    auto_scale_on_surge: bool = True


class ApiKeysConfig(BaseModel):
    ncbi_api_key_set: bool = True
    ncbi_api_key_masked: str = "ncbi_live_9f8...a21"
    llm_api_key_set: bool = True
    llm_api_key_masked: str = "sk-llm-...78b"
    alphafold_service_key_masked: str = "af3_svc_...d09"
    colabfold_server_url: str = "https://colabfold.cloud.gov.au/api"
    gisaid_access_token_masked: str = "gis_token_...f54"


class GovernanceSettings(BaseModel):
    classification: SecurityClassification = SecurityClassification.OFFICIAL_SENSITIVE
    compliance: ComplianceFramework = Field(default_factory=ComplianceFramework)
    compute: CloudComputeConfig = Field(default_factory=CloudComputeConfig)
    api_keys: ApiKeysConfig = Field(default_factory=ApiKeysConfig)
    data_custodian: str = "Commonwealth Emergency Response Data Custodian"
    retention_period_years: int = 7
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
