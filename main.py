from src.logger.custom_logging import logger
from src.exception.exception import CustomException
from src.pipeline.dataingestion import DataIngestionPipe
from src.pipeline.datatransform import DataTransfromPipe
from src.pipeline.modeltrainer import ModelTrainerPipe
from src.pipeline.modeleval import ModelEvalPipe
from src.pipeline.modelpusher import ModelPusherPipe
import sys

def run_stage(stage_name, pipeline_class,*args):
    try:
        logger.info(f">>>>>> stage {stage_name} started <<<<<<")
        pipeline = pipeline_class(*args)
        artifact=pipeline.main()
        logger.info(f">>>>>> stage {stage_name} completed <<<<<<\n\nx==========x")
        return artifact
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)
    
if __name__ == "__main__":
 
    # Stage 1: Data Ingestion
    data_ingestion_artifact = run_stage("Data Ingestion", DataIngestionPipe)  

    # Stage 2: Data Transformation
    data_transformation_artifact = run_stage("Data Transformation", DataTransfromPipe, data_ingestion_artifact)

    # Stage 3: Model Trainer
    model_Trainer_artifact=run_stage('Model Trainer',ModelTrainerPipe,data_transformation_artifact)

    # Stage 4: Model Evaluation
    model_Eval_Artifact=run_stage('Model Evaluation',ModelEvalPipe,data_transformation_artifact,model_Trainer_artifact)

    # Stage5: Model Pusher
    run_stage('Model Pusher',ModelPusherPipe,model_Trainer_artifact)

