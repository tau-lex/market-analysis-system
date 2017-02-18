#include "include/masopennnclasses.h"

// ADD INPUT METHOD

/// Add input method
/// Method added one new input layer.
/// @param new_layer_size Number of inputs and neurons in this input layer.

void MASNeuralNetwork::add_input(const size_t& new_layer_size)
{
    Vector<PerceptronLayer*> perceptron_layers;
    perceptron_layers.push_back(new PerceptronLayer(new_layer_size, new_layer_size));
    inputs_layers_pointers.push_back(perceptron_layers);

    size_t new_input_size = 0;
    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++)
        new_input_size += inputs_layers_pointers[idx][0]->get_inputs_number();
    if( !inputs_pointer )
        inputs_pointer = new Inputs();
    inputs_pointer->set(new_input_size);
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
    perceptron_layers.push_back(new PerceptronLayer(new_inputs_number, new_layer_size));
    inputs_layers_pointers.push_back(perceptron_layers);

    size_t new_input_size = 0;
    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++)
        new_input_size += inputs_layers_pointers[idx][0]->get_inputs_number();
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
    Vector<PerceptronLayer*> perceptron_layers;
    // Main input
    perceptron_layers.push_back(new PerceptronLayer(new_inputs_number, new_layer_size));
    // Sum input and recurent layers
    perceptron_layers.push_back(new PerceptronLayer(new_layer_size, new_layer_size));
    // Recurent layers
    for(size_t idx = 0; idx < new_depth_recursion; idx++) {
        perceptron_layers.push_back(new PerceptronLayer(new_layer_size, new_layer_size));
        Vector<double> history_vec(new_layer_size, 0.0);
        memory_outputs_data.push_back(history_vec);
    }
    inputs_layers_pointers.push_back(perceptron_layers);

    size_t new_input_size = 0;
    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++)
        new_input_size += inputs_layers_pointers[idx][0]->get_inputs_number();
    if( !inputs_pointer )
        inputs_pointer = new Inputs();
    inputs_pointer->set(new_input_size);
}

void MASNeuralNetwork::construct_inputs()
{
    if(!inputs_pointer)
    {
        size_t inputs_number = 0;

        for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++)
            inputs_number += inputs_layers_pointers[idx][0]->get_inputs_number();

        inputs_pointer = new Inputs(inputs_number);
    }
}

size_t MASNeuralNetwork::count_parameters_number() const
{
    size_t parameters_number = 0;

    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++) {
        for(size_t idxin = 0; idxin < inputs_layers_pointers[idx].size(); idxin++) {
            parameters_number += inputs_layers_pointers[idx][idxin]->count_parameters_number();
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

    for(size_t idx = 0; idx < outputs_layers_pointers.size(); idx++) {
        parameters_number += outputs_layers_pointers[idx]->count_parameters_number();
    }

    return(parameters_number);
}

Vector<double> MASNeuralNetwork::arrange_parameters() const
{
    Vector<double> parameters;

    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++) {
        for(size_t idxin = 0; idxin < inputs_layers_pointers[idx].size(); idxin++) {
            parameters.assemble(inputs_layers_pointers[idx][idxin]->arrange_parameters());
        }
    }

    if( multilayer_perceptron_pointer )
        parameter.assemble(multilayer_perceptron_pointer->arrange_parameters());
    if( independent_parameters_pointer )
        parameter.assemble(independent_parameters_pointer->calculate_scaled_parameters());

    for(size_t idx = 0; idx < outputs_layers_pointers.size(); idx++) {
        parameters.assemble(outputs_layers_pointers[idx]->arrange_parameters());
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

    for(size_t idx = 0; idx < inputs_layers_pointers.size(); idx++) {
        for(size_t idxin = 0; idxin < inputs_layers_pointers[idx].size(); idxin++) {
            parameters_number = inputs_layers_pointers[idx][idxin]->count_parameters_number();
            const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
            inputs_layers_pointers[idx][idxin]->set_parameters(parameters);
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

    for(size_t idx = 0; idx < outputs_layers_pointers.size(); idx++) {
        parameters_number = outputs_layers_pointers[idx]->count_parameters_number();
        const Vector<double> parameters = new_parameters.take_out(take_begin,parameters_number);
        outputs_layers_pointers[idx]->set_parameters(parameters);
        take_begin += parameters_number;
    }
}

void MASNeuralNetwork::add_output(const size_t& new_layer_size)
{
    size_t inputs_number = 0;
    if( multilayer_perceptron_pointer )
        inputs_number = multilayer_perceptron_pointer->get_outputs_number();
    outputs_layers_pointers.push_back(new PerceptronLayer(inputs_number, new_layer_size));

    size_t new_output_size = 0;
    for(size_t idx = 0; idx < outputs_layers_pointers.size(); idx++)
        new_output_size += outputs_layers_pointers[idx]->get_perceptrons_number();
    if( !outputs_pointer )
        outputs_pointer = new Outputs();
    outputs_pointer->set(new_output_size);
}

void MASNeuralNetwork::construct_outputs()
{
    if(!outputs_pointer)
    {
        size_t outputs_number = 0;

        for(size_t idx = 0; idx < outputs_layers_pointers.size(); idx++)
            outputs_number += outputs_layers_pointers[idx]->get_perceptrons_number();

        outputs_pointer = new Outputs(outputs_number);
    }
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

    Vector<double> outputs(inputs);

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
    size_t take_size, take_begin = 0;
    Vector<Vector<double> > outputs_input_layer;

    for( size_t idx = 0; idx < inputs_layers_pointers.size(); idx++ ) {

        Vector<double> tmp_vec;
        take_size = inputs_layers_pointers[idx][0]->get_inputs_number();
        Vector<double> tmp_invec = outputs.take_out( take_begin, take_size );

        if( inputs_layers_pointers[idx].size() == 1 ) {

            tmp_vec = inputs_layers_pointers[idx][0]->calculate_outputs( tmp_invec );

        } else if( inputs_layers_pointers[idx].size() >= 3 ) {

            tmp_vec = inputs_layers_pointers[idx][0]->calculate_outputs( tmp_invec );

            Vector<double> tmp_histvec;

            for( size_t idxhist = 2; idxhist < inputs_layers_pointers[idx].size(); idxhist++ ) {
                // ?
                tmp_histvec = inputs_layers_pointers[idx][idxhist]->calculate_outputs(/* ? */);
                // ?
            }

            tmp_vec.assemble( tmp_histvec );

            tmp_vec = inputs_layers_pointers[idx][1]->calculate_outputs( tmp_vec );

        } else { /* err */; }

        outputs_input_layer.push_back( tmp_vec );
    }

    outputs.clear();
    foreach( auto vec, outputs_input_layer ) {
        outputs.assemble( vec );
    }

    // Multilayer perceptron

    if(multilayer_perceptron_pointer)
    {
        outputs = multilayer_perceptron_pointer->calculate_outputs(outputs);
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

Matrix<double> MASNeuralNetwork::calculate_output_data(const Matrix<double> &) const
{

}

void MASNeuralNetwork::save(const std::string &) const
{

}

void MASNeuralNetwork::load(const std::string &)
{

}
