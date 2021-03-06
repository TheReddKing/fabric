echo "evaluating v50 static"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v50_n100_i8.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v50_n100_i8_static.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v50_n100_i8_static.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
echo "evaluating v50 dynamic"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v50_n100_i8_csv.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v50_n100_i8_dynamic.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v50_n100_i8_dynamic.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
echo "evaluating v100 static"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v100_n100_i8.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v100_n100_i8_static.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v100_n100_i8_static.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
echo "evaluating v100 dynamic"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v100_n100_i8_csv.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v100_n100_i8_dynamic.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v100_n100_i8_dynamic.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
echo "evaluating v300 static"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v300_n100_i8.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v300_n100_i8_static.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v300_n100_i8_static.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
echo "evaluating v300 dynamic"
python run_relemb_evaluator.py --we_model /data/kevin21/testing/mitall/allvectors/mitall_v300_n100_i8_csv.txt --rel_emb /data/raulcf/relemb/mitdwh/mitall_v300_n100_i8_dynamic.pkl --data /data/raulcf/datasets/mitdwhdataall/ --output results_v300_n100_i8_dynamic.log --eval_table Employee_directory.csv --entity_attribute "Mit Id" --target_attribute "First Name"
