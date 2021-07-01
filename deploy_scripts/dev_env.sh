export ENV="dev"

# ----- VPC ----- #
# CIDR
export CIDR="10.10.0.0/16"
# CIDR mask
export CIDR_MASK="20"
# Max AZs
export MAX_AZS="2"

# ----- Aurora ----- #
# Aurora database name (a-zA-Z0-9_)
export DB_NAME="eUni"
# Aurora master username
export DB_MASTER_USERNAME="eUni_admin"
# Aurora max ACU
export DB_MAX_ACU="2"
# Aurora min ACU
export DB_MIN_ACU="2"

# ----- API ----- #
export API_STAGE_NAME="dev"
export LOG_LEVEL="DEBUG"  # debug/info/error

# ---------------------------------------------------------------
# You probably don't need to change these values
export APP_NAME="eUni"
export LAMBDAS_DIR="lambdas"