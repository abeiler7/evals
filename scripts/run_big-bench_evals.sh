while getopts 'm:e:d:v:' flag;
do
	case "${flag}" in
		m) model_id="${OPTARG}";;
		e) eval_arg="${OPTARG}";;
		d) dir="${OPTARG}";;
		v) ver="${OPTARG}";;
	esac
done
if [ -v $dir ]
then
	dir="/student/abeiler/evaluation_data"
fi
if [ -v $ver ]
then
	ver="v1"
fi

echo "Model: $model_id";
echo "Eval: $eval_arg";
echo "Logs & Records Dir: $dir"
if [ $eval_arg == "ALL" ]
then
	evals=( 
		bb-arithmetic-1_digit_addition
		bb-arithmetic-2_digit_addition
		bb-arithmetic-3_digit_addition
		bb-arithmetic-4_digit_addition
		bb-arithmetic-5_digit_addition
		bb-arithmetic-1_digit_subtraction 
		bb-arithmetic-2_digit_subtraction
		bb-arithmetic-3_digit_subtraction
		bb-arithmetic-4_digit_subtraction
		bb-arithmetic-5_digit_subtraction
		bb-arithmetic-1_digit_multiplication
		bb-arithmetic-2_digit_multiplication
		bb-arithmetic-3_digit_multiplication
		bb-arithmetic-4_digit_multiplication
		bb-arithmetic-5_digit_multiplication
		bb-arithmetic-1_digit_division
		bb-arithmetic-2_digit_division
		bb-arithmetic-3_digit_division 
		bb-arithmetic-4_digit_division
		bb-arithmetic-5_digit_division
	 )
elif [ $eval_arg == "MULT" ]
then
	evals=( 
		bb-arithmetic-1_digit_multiplication
		bb-arithmetic-2_digit_multiplication
		bb-arithmetic-3_digit_multiplication
		bb-arithmetic-4_digit_multiplication
		bb-arithmetic-5_digit_multiplication
	)
elif [ $eval_arg == "ADD" ]
then
	evals=( 
		bb-arithmetic-1_digit_addition
		bb-arithmetic-2_digit_addition
		bb-arithmetic-3_digit_addition
		bb-arithmetic-4_digit_addition
		bb-arithmetic-5_digit_addition
	)
elif [ $eval_arg == "SUB" ]
then
	evals=( 
		bb-arithmetic-1_digit_subtraction 
		bb-arithmetic-2_digit_subtraction
		bb-arithmetic-3_digit_subtraction
		bb-arithmetic-4_digit_subtraction
		bb-arithmetic-5_digit_subtraction
	)
elif [ $eval_arg == "DIV" ]
then
	evals=( 
		bb-arithmetic-1_digit_division
		bb-arithmetic-2_digit_division
		bb-arithmetic-3_digit_division 
		bb-arithmetic-4_digit_division
		bb-arithmetic-5_digit_division
	)
else
	evals=( $eval_arg )
fi

if [ ! -d "$dir/logs/$model_id-$ver" ]
then
	echo "Model Directory Does Not Exist in logs. Creating Now."
	mkdir -p $dir/logs/$model_id\-$ver
else
	echo "Model Directory Already Exists in logs."
fi

if [ ! -d "$dir/records/$model-$vid" ]
then
	echo "Model Directory Does Not Exist in records. Creating Now."
	mkdir -p $dir/records/$model_id-$ver
else
	echo "Model Directory Already Exists in records."
fi


for e in "${evals[@]}"
do
	echo "oaieval --log_to_file $dir/logs/$model_id-$ver/$e.jsonl --record_path $dir/records/$model_id-$ver/$e.jsonl llama2/finetuned/$model_id $e"
	oaieval --log_to_file $dir/logs/$model_id-$ver/$e.jsonl --record_path $dir/records/$model_id-$ver/$e.jsonl llama2/finetuned/$model_id $e
done
