#!/bin/bash

# CloudFormation Deployment Script for Cloud-Native App
# This script deploys the infrastructure using CloudFormation YAML template

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
STAGE=${STAGE:-dev}
SERVICE_NAME=${SERVICE_NAME:-student-factory}
AWS_REGION=${AWS_REGION:-us-west-2}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-123456789012}
TEMPLATE_FILE="cloudformation-template.yaml"
STACK_NAME="${SERVICE_NAME}-${STAGE}"

# Load environment variables from env directory
ENV_FILE="env/.env.${STAGE}"
if [ -f "$ENV_FILE" ]; then
    print_status "Loading environment configuration from: $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    print_warning "Environment file $ENV_FILE not found, using defaults"
fi

# Function to check if AWS CLI is installed and configured
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi

    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS CLI is not configured. Please run 'aws configure' first."
        exit 1
    fi

    print_success "AWS CLI is installed and configured"
}

# Function to check if template file exists
check_template() {
    if [ ! -f "$TEMPLATE_FILE" ]; then
        print_error "Template file $TEMPLATE_FILE not found"
        exit 1
    fi
    print_success "Template file found: $TEMPLATE_FILE"
}

# Function to validate CloudFormation template
validate_template() {
    print_status "Validating CloudFormation template..."
    
    if aws cloudformation validate-template --template-body file://$TEMPLATE_FILE --region $AWS_REGION > /dev/null 2>&1; then
        print_success "Template validation successful"
    else
        print_error "Template validation failed"
        aws cloudformation validate-template --template-body file://$TEMPLATE_FILE --region $AWS_REGION
        exit 1
    fi
}

# Function to check if stack exists
stack_exists() {
    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION > /dev/null 2>&1
}

# Function to deploy stack
deploy_stack() {
    local operation=$1
    
    print_status "Deploying stack: $STACK_NAME"
    print_status "Stage: $STAGE"
    print_status "Service: $SERVICE_NAME"
    print_status "Region: $AWS_REGION"
    print_status "Account: $AWS_ACCOUNT_ID"
    
    local parameters="ParameterKey=Stage,ParameterValue=$STAGE"
    parameters="$parameters ParameterKey=ServiceName,ParameterValue=$SERVICE_NAME"
    parameters="$parameters ParameterKey=AWSAccountId,ParameterValue=$AWS_ACCOUNT_ID"
    parameters="$parameters ParameterKey=AWSRegion,ParameterValue=$AWS_REGION"
    
    if [ "$operation" = "create" ]; then
        print_status "Creating new stack..."
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --parameters $parameters \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $AWS_REGION \
            --tags Key=Environment,Value=$STAGE Key=Service,Value=$SERVICE_NAME Key=Owner,Value="Dan Holman" Key=Project,Value="Portfolio"
    else
        print_status "Updating existing stack..."
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://$TEMPLATE_FILE \
            --parameters $parameters \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $AWS_REGION
    fi
    
    print_status "Waiting for stack operation to complete..."
    aws cloudformation wait stack-${operation}-complete --stack-name $STACK_NAME --region $AWS_REGION
    
    if [ $? -eq 0 ]; then
        print_success "Stack $operation completed successfully"
    else
        print_error "Stack $operation failed"
        exit 1
    fi
}

# Function to show stack outputs
show_outputs() {
    print_status "Retrieving stack outputs..."
    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION --query 'Stacks[0].Outputs' --output table
}

# Function to show stack events
show_events() {
    print_status "Recent stack events:"
    aws cloudformation describe-stack-events --stack-name $STACK_NAME --region $AWS_REGION --query 'StackEvents[0:10].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId,ResourceStatusReason]' --output table
}

# Function to delete stack
delete_stack() {
    print_warning "This will delete the entire stack: $STACK_NAME"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Deleting stack: $STACK_NAME"
        aws cloudformation delete-stack --stack-name $STACK_NAME --region $AWS_REGION
        
        print_status "Waiting for stack deletion to complete..."
        aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME --region $AWS_REGION
        
        if [ $? -eq 0 ]; then
            print_success "Stack deleted successfully"
        else
            print_error "Stack deletion failed"
            exit 1
        fi
    else
        print_status "Stack deletion cancelled"
    fi
}

# Function to show help
show_help() {
    echo "CloudFormation Deployment Script for Cloud-Native App"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy     Deploy or update the stack (default)"
    echo "  create     Create a new stack"
    echo "  update     Update existing stack"
    echo "  delete     Delete the stack"
    echo "  status     Show stack status and outputs"
    echo "  events     Show recent stack events"
    echo "  validate   Validate the CloudFormation template"
    echo "  help       Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  STAGE           Deployment stage (dev/staging/prod) [default: dev]"
    echo "  SERVICE_NAME    Service name prefix [default: student-factory]"
    echo "  AWS_REGION      AWS region [default: us-west-2]"
    echo "  AWS_ACCOUNT_ID  AWS account ID [default: 123456789012]"
    echo ""
    echo "Examples:"
    echo "  $0 deploy                    # Deploy with default settings"
    echo "  STAGE=prod $0 deploy         # Deploy to production"
    echo "  $0 delete                    # Delete the stack"
    echo "  $0 status                    # Show stack status"
}

# Main script logic
main() {
    local command=${1:-deploy}
    
    case $command in
        deploy)
            check_aws_cli
            check_template
            validate_template
            
            if stack_exists; then
                deploy_stack "update"
            else
                deploy_stack "create"
            fi
            
            show_outputs
            ;;
        create)
            check_aws_cli
            check_template
            validate_template
            
            if stack_exists; then
                print_error "Stack $STACK_NAME already exists. Use 'update' or 'deploy' instead."
                exit 1
            fi
            
            deploy_stack "create"
            show_outputs
            ;;
        update)
            check_aws_cli
            check_template
            validate_template
            
            if ! stack_exists; then
                print_error "Stack $STACK_NAME does not exist. Use 'create' or 'deploy' instead."
                exit 1
            fi
            
            deploy_stack "update"
            show_outputs
            ;;
        delete)
            check_aws_cli
            delete_stack
            ;;
        status)
            check_aws_cli
            if stack_exists; then
                show_outputs
            else
                print_error "Stack $STACK_NAME does not exist"
                exit 1
            fi
            ;;
        events)
            check_aws_cli
            if stack_exists; then
                show_events
            else
                print_error "Stack $STACK_NAME does not exist"
                exit 1
            fi
            ;;
        validate)
            check_aws_cli
            check_template
            validate_template
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
