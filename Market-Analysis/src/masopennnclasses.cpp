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

void MASNeuralNetwork::set_parameters(const Vector<double> &)
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
}

Vector<double> MASNeuralNetwork::calculate_outputs(const Vector<double> &, const Vector<double> &) const
{

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
