provider "aws" {
  region = "us-east-1" # Substitua pela sua região desejada
}

resource "aws_cloudwatch_metric_alarm" "example_alarm" {
  alarm_name          = "example-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods = 1
  metric_name        = "CPUUtilization" # Substitua pelo nome da métrica desejada
  namespace          = "AWS/EC2"        # Substitua pelo namespace correto
  period             = 60
  statistic           = "Average"
  threshold          = 90
  alarm_description  = "This metric should trigger a Lambda function."
  alarm_actions      = [aws_lambda_function.example_lambda.arn]
}

resource "aws_ssm_parameter" "example_parameter" {
  name        = "/example/parameter"
  description = "Example SSM parameter"
  type        = "String"
  value       = "ExampleValue" # Substitua pelo valor desejado
}

resource "aws_lambda_function" "example_lambda" {
  filename      = "lambda.zip" # Substitua pelo nome do seu arquivo zip do código da Lambda
  function_name = "example_lambda"
  role          = aws_iam_role.example_lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x" # Substitua pela versão de runtime desejada

  environment {
    variables = {
      PARAMETER_NAME = aws_ssm_parameter.example_parameter.name
    }
  }
}

resource "aws_iam_role" "example_lambda_role" {
  name = "example_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_permission" "example_lambda_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.example_lambda.function_name
  principal     = "events.amazonaws.com"

  source_arn = aws_cloudwatch_metric_alarm.example_alarm.arn
}
