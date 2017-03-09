import os
import boto3


def lambda_handler(event, context):
  transcoder = boto3.client('elastictranscoder', 'us-east-1')
  pipeline_id = get_pipeline(transcoder, 'transcoder')
  base_filename = os.path.basename(event['Records'][0]['s3']['object']['key'])
  output = transcoder.create_job(
      PipelineId=pipeline_id,
      Input={
          'Key': create_aws_filename('uploads', base_filename, ''),
          'FrameRate': 'auto',
          'Resolution': 'auto',
          'AspectRatio': 'auto',
          'Interlaced': 'auto',
          'Container' : 'auto'
      },
      Outputs=[{
          'Key': create_aws_filename('transcoded', base_filename, '-generic-1080p.mp4'),
          'PresetId': '1351620000001-000001'
          }, {
          'Key': create_aws_filename('transcoded', base_filename, '-generic-720p.mp4'),
          'PresetId': '1351620000001-000010'
          }, {
          'Key': create_aws_filename('transcoded', base_filename, '-FullHD1080i60.mp4'),
          'PresetId': '1351620000001-100180'
          }, {
          'Key': create_aws_filename('transcoded', base_filename, '-web.mp4'),
          'PresetId': '1351620000001-100070'
          }
      ]
  )
  return output


def get_pipeline(transcoder, pipeline_name):
      paginator = transcoder.get_paginator('list_pipelines')
      for page in paginator.paginate():
          for pipeline in page['Pipelines']:
              if pipeline['Name'] == pipeline_name:
                  return pipeline['Id']


def create_aws_filename(folder, filename, extension):
      aws_filename = os.path.join(
          folder, filename + extension
      )
      return aws_filename
