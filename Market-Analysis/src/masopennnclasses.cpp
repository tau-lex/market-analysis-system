#include "include/masopennnclasses.h"

// ADD INPUT METHOD

/// Add input method
/// Method added one new input layer.
/// @param new_layer_size Number of inputs and neurons in this input layer.

void MASNeuralNetwork::add_input(const size_t& new_layer_size)
{
    add_input( new_layer_size, new_layer_size );
}

// ADD INPUT METHOD

/// Add input method
/// Method added one new input layer.
/// @param new_inputs_number Number of inputs in the multilayer perceptron
/// @param new_layer_size Number of inputs and neurons in this input layer.

void MASNeuralNetwork::add_input(const size_t& new_inputs_number,
                                 const size_t& new_layer_size)
{
    Vector<PerceptronLayer*> perceptron_layers;
    Vector< Vector<double> > tmpHistVec;
    perceptron_layers.push_back(new PerceptronLayer(new_inputs_number, new_layer_size));
    inputsArrayPtr.push_back(perceptron_layers);
    memoryHistoryData.push_back( tmpHistVec );

    size_t new_input_size = 0;
    for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++)
        new_input_size += inputsArrayPtr[idx][0]->get_inputs_number();
    if( !inputs_pointer )
        inputs_pointer = new Inputs();
    inputs_pointer->set(new_input_size);
}

// ADD INPUT METHOD

/// Add input method
/// Method added new input layer with a recurent layers for history.
/// @param new_inputs_number Number of inputs in the multilayer perceptron
/// @param new_layer_size Number of inputs and neurons in this input layer.
/// @param new_depth_recursion Number of perceptron layers in recursion section.

void MASNeuralNetwork::add_input(const size_t& new_inputs_number,
                                 const size_t& new_layer_size,
                                 const size_t& new_depth_recursion)
{
    Vector<PerceptronLayer*> newInputLayer;
    Vector< Vector<double> > tmpHistVec;
    // Main input
    newInputLayer.push_back( new PerceptronLayer(new_inputs_number, new_layer_size) );
    // Sum input and recurent layers
    newInputLayer.push_back( new PerceptronLayer(new_layer_size*2, new_layer_size) );
    // Recurent layers
    for(size_t idx = 0; idx < new_depth_recursion; idx++) {
        if( idx < new_depth_recursion-1  )
            newInputLayer.push_back( new PerceptronLayer(new_layer_size*2, new_layer_size) );
        else
            newInputLayer.push_back( new PerceptronLayer(new_layer_size, new_layer_size) );
        Vector<double> newHistoryVec( new_layer_size , 0.0 );
        tmpHistVec.push_back( newHistoryVec );
    }
    inputsArrayPtr.push_back( newInputLayer );
    memoryHistoryData.push_back( tmpHistVec );

    size_t new_input_size = 0;
    for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++)
        new_input_size += inputsArrayPtr[idx][0]->get_inputs_number();
    if( !inputs_pointer )
        inputs_pointer = new Inputs();
    inputs_pointer->set(new_input_size);
}

void MASNeuralNetwork::construct_inputs()
{
    if(!inputs_pointer)
    {
        size_t inputs_number = 0;

        for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++)
            inputs_number += inputsArrayPtr[idx][0]->get_inputs_number();

        inputs_pointer = new Inputs(inputs_number);
    }
}

size_t MASNeuralNetwork::get_inputs_number()
{

}

size_t MASNeuralNetwork::count_parameters_number() const
{
    size_t parameters_number = 0;

    for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++) {
        for(size_t idxin = 0; idxin < inputsArrayPtr[idx].size(); idxin++) {
            parameters_number += inputsArrayPtr[idx][idxin]->count_parameters_number();
        }
    }

    if(multilayer_perceptron_pointer)
    {
        parameters_number += multilayer_perceptron_pointer->count_parameters_number();
    }

    if(independent_parameters_pointer)
    {
        parameters_number += independent_parameters_pointer->get_parameters_number();
    }

    for(size_t idx = 0; idx < outputsArrayPtr.size(); idx++) {
        parameters_number += outputsArrayPtr[idx]->count_parameters_number();
    }

    return(parameters_number);
}

Vector<double> MASNeuralNetwork::arrange_parameters() const
{
    Vector<double> parameters;

    for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++) {
        for(size_t idxin = 0; idxin < inputsArrayPtr[idx].size(); idxin++) {
            parameters.assemble(inputsArrayPtr[idx][idxin]->arrange_parameters());
        }
    }

    if( multilayer_perceptron_pointer )
        parameter.assemble(multilayer_perceptron_pointer->arrange_parameters());
    if( independent_parameters_pointer )
        parameter.assemble(independent_parameters_pointer->calculate_scaled_parameters());

    for(size_t idx = 0; idx < outputsArrayPtr.size(); idx++) {
        parameters.assemble(outputsArrayPtr[idx]->arrange_parameters());
    }

    return(parameters);
}

void MASNeuralNetwork::set_parameters(const Vector<double>& new_parameters)
{
    // Control sentence (if debug)

#ifdef __OPENNN_DEBUG__

    const size_t size = new_parameters.size();

    const size_t parameters_number = count_parameters_number();

    if(size != parameters_number)
    {
        std::ostringstream buffer;

        buffer << "OpenNN Exception: NeuralNetwork class.\n"
               << "void set_parameters(const Vector<double>&) method.\n"
               << "Size must be equal to number of parameters.\n";

        throw std::logic_error(buffer.str());
    }

#endif

    size_t parameters_number, take_begin = 0;

    for(size_t idx = 0; idx < inputsArrayPtr.size(); idx++) {
        for(size_t idxin = 0; idxin < inputsArrayPtr[idx].size(); idxin++) {
            parameters_number = inputsArrayPtr[idx][idxin]->count_parameters_number();
            const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
            inputsArrayPtr[idx][idxin]->set_parameters(parameters);
            take_begin += parameters_number;
        }
    }

    if(multilayer_perceptron_pointer)
    {
        parameters_number = multilayer_perceptron_pointer->count_parameters_number();
        const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
        multilayer_perceptron_pointer->set_parameters(parameters);
        take_begin += parameters_number;
    }

    if(independent_parameters_pointer)
    {
        parameters_number = independent_parameters_pointer->get_parameters_number();
        const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
        independent_parameters_pointer->unscale_parameters(parameters);
        take_begin += parameters_number;
    }

    for(size_t idx = 0; idx < outputsArrayPtr.size(); idx++) {
        parameters_number = outputsArrayPtr[idx]->count_parameters_number();
        const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
        outputsArrayPtr[idx]->set_parameters(parameters);
        take_begin += parameters_number;
    }
}

void MASNeuralNetwork::add_output(const size_t& new_layer_size)
{
    size_t inputs_number = 0;
    if( multilayer_perceptron_pointer )
        inputs_number = multilayer_perceptron_pointer->get_outputs_number();
    else
        throw std::logic_error("Prepare first a multilayer perceptron!");
    outputsArrayPtr.push_back(new PerceptronLayer(inputs_number, new_layer_size));

    size_t new_output_size = 0;
    for(size_t idx = 0; idx < outputsArrayPtr.size(); idx++)
        new_output_size += outputsArrayPtr[idx]->get_perceptrons_number();
    if( !outputs_pointer )
        outputs_pointer = new Outputs();
    outputs_pointer->set(new_output_size);
}

void MASNeuralNetwork::construct_outputs()
{
    if(!outputs_pointer)
    {
        size_t outputs_number = 0;

        for(size_t idx = 0; idx < outputsArrayPtr.size(); idx++)
            outputs_number += outputsArrayPtr[idx]->get_perceptrons_number();

        outputs_pointer = new Outputs(outputs_number);
    }
}

size_t MASNeuralNetwork::get_outputs_number()
{

}

Vector<double> MASNeuralNetwork::calculate_outputs(const Vector<double>& inputs) const
{
    // Control sentence (if debug)

#ifdef __OPENNN_DEBUG__

    if(multilayer_perceptron_pointer)
    {
        const size_t inputs_size = inputs.size();

        const size_t inputs_number = multilayer_perceptron_pointer->get_inputs_number();

        if(inputs_size != inputs_number)
        {
            std::ostringstream buffer;

            buffer << "OpenNN Exception: NeuralNetwork class.\n"
                   << "Vector<double> calculate_outputs(const Vector<double>&) const method.\n"
                   << "Size of inputs must be equal to number of inputs.\n";

            throw std::logic_error(buffer.str());
        }
    }

#endif

    Vector<double> outputs( inputs );

    // Scaling layer

    if( scaling_layer_pointer )
    {
        outputs = scaling_layer_pointer->calculate_outputs( inputs );
    }

    // Principal components layer

    if( principal_components_layer_pointer )
    {
       outputs = principal_components_layer_pointer->calculate_outputs( outputs );
    }

    // MAS Inputs

    size_t takeSize, takeBegin = 0; // for take_out from a input
    Vector< Vector<double> > outputsArray; // outputs from input layers

    for( size_t idx = 0; idx < inputsArrayPtr.size(); idx++ ) {
        Vector<double> tmpInVec, tmpOutVec;
        takeSize = inputsArrayPtr[idx][0]->get_inputs_number();
        tmpInVec = outputs.take_out( takeBegin, takeSize );
        takeBegin = takeSize;

        if( inputsArrayPtr[idx].size() == 1 ) { // without history layers
            tmpOutVec = inputsArrayPtr[idx][0]->calculate_outputs( tmpInVec );
        } else if( inputsArrayPtr[idx].size() >= 3 ) { //with history layers
            // calculate input layer
            tmpOutVec = inputsArrayPtr[idx][0]->calculate_outputs( tmpInVec );
            // calculate history layer
            Vector<double> tmpHistVec;
            for( size_t idxHist = inputsArrayPtr[idx].size()-1; idxHist >= 2; idxHist-- ) {
                // from endHistory to current-1(beginHistory)
                if( idxHist == inputsArrayPtr[idx].size()-1 ) {// if last history layer
                    tmpHistVec = inputsArrayPtr[idx][idxHist]->
                            calculate_outputs( memoryHistoryData[idx][idxHist-2] );
                } else {// if not last history layer
                    tmpHistVec = inputsArrayPtr[idx][idxHist]->
                            calculate_outputs( tmpHistVec.assemble(memoryHistoryData[idx][idxHist-2]) );
                    memoryHistoryData[idx][idxHist-1] = tmpHistVec;
                }
            }
            memoryHistoryData[idx][0] = tmpOutVec;
            tmpOutVec.assemble( tmpHistVec );
            // calulate output layer
            tmpOutVec = inputsArrayPtr[idx][1]->calculate_outputs( tmpOutVec );
        } else {
            throw std::logic_error("MASNeuralNetwork::calculate_outputs()");
        }
        outputsArray.push_back( tmpOutVec );
    }
    outputs.clear();
    foreach( auto vec, outputsArray ) {
        outputs.assemble( vec );
    }

    // Multilayer perceptron

    if(multilayer_perceptron_pointer)
    {
        outputs = multilayer_perceptron_pointer->calculate_outputs(outputs);
    }

    // MAS Outputs

    takeSize = 0, takeBegin = 0; // for take_out from a output a multilayer perceptron
    outputsArray.clear(); // outputs from output layers

    size_t inSize = 0;
    for( size_t idx = 0; idx < outputsArrayPtr.size(); idx++ )
        inSize += outputsArrayPtr[idx]->get_inputs_number();
    if( multilayer_perceptron_pointer->get_outputs_number() != inSize )
        throw std::logic_error(" MLP.out != OutputsSumIn ");

    for( size_t idx = 0; idx < outputsArrayPtr.size(); idx++ ) {
        Vector<double> tmpVec;
        takeSize = outputsArrayPtr[idx]->get_inputs_number();
        tmpVec = outputs.take_out( takeBegin, takeSize );
        takeBegin = takeSize;
        // calculate output layer
        tmpVec = outputsArrayPtr[idx]->calculate_outputs( tmpVec );
        outputsArray.push_back( tmpVec );
    }
    outputs.clear();
    foreach( auto vec, outputsArray ) {
        outputs.assemble( vec );
    }

    // Conditions

    if(conditions_layer_pointer)
    {
        outputs = conditions_layer_pointer->calculate_outputs(inputs, outputs);
    }

    // Unscaling layer

    if(unscaling_layer_pointer)
    {
        outputs = unscaling_layer_pointer->calculate_outputs(outputs);
    }

    // Probabilistic layer

    if(probabilistic_layer_pointer)
    {
        outputs = probabilistic_layer_pointer->calculate_outputs(outputs);
    }

    // Bounding layer

    if(bounding_layer_pointer)
    {
        outputs = bounding_layer_pointer->calculate_outputs(outputs);
    }

    return(outputs);
}

Matrix<double> MASNeuralNetwork::calculate_output_data(const Matrix<double>& input_data) const
{
    const size_t inputs_number = get_inputs_number();
    const size_t outputs_number = get_outputs_number();

    // Control sentence (if debug)

#ifdef __OPENNN_DEBUG__

    const size_t columns_number = input_data.get_columns_number();

    if(columns_number != inputs_number)
    {
        std::ostringstream buffer;

        buffer << "OpenNN Exception: NeuralNetwork class.\n"
               << "Matrix<double> calculate_output_data(const Matrix<double>&) const method.\n"
               << "Number of columns must be equal to number of inputs.\n";

        throw std::logic_error(buffer.str());
    }

#endif

    const size_t input_vectors_number = input_data.get_rows_number();

    Matrix<double> output_data(input_vectors_number, outputs_number);

    Vector<double> inputs(inputs_number);
    Vector<double> outputs(outputs_number);

//#pragma omp parallel for private(inputs, outputs)

    for(int i = 0; i < input_vectors_number; i++)
    {
        inputs = input_data.arrange_row(i);
        outputs = calculate_outputs(inputs);
        output_data.set_row(i, outputs);
    }

    return(output_data);
}

void MASNeuralNetwork::save(const std::string &) const
{

}

void MASNeuralNetwork::load(const std::string &)
{

}
