resource "aws_iam_role" "stock_role" {
  name = "stock-instance-role"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [{
      Effect : "Allow",
      Principal : {
        Service : "ec2.amazonaws.com"
      },
      Action : "sts:AssumeRole"
    }]
  })
}
resource "aws_iam_policy" "stock_policy" {
  name = "stock-policy"
  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Action : [
          "s3:*",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource : "*"
      }
    ]
  })
}
resource "aws_iam_policy" "stock_acces_policy" {
  name = "stock-acces-policy"
  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : [
            "ec2:RunInstances",
            "ec2:DescribeInstances",
            "ec2:CreateTags",
            "iam:PassRole"
          ],
          "Resource" : "*"
        }
      ]
  })


}
resource "aws_iam_role_policy_attachment" "stock_policy_attach" {
    role= aws_iam_role.stock_role.name
    policy_arm= aws_iam_policy.stock_policy.arm
  
}

resource "aws_iam_role_policy_attachment" "stock_access_policy_attach" {

    role= aws_iam_role.stock_role.name
    policy_arn=aws_iam_policy.stock_acces_policy.arn
  
}
resource "aws_instence_profile" "stock_instance_profile" {
    name=stock-instence-profile
    role=aws_iam_role.stock_role.name
  
}

