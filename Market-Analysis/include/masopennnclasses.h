#ifndef MASOPENNNCLASSES_H
#define MASOPENNNCLASSES_H

// include opennn library
#include "../opennn/opennn.h"
using namespace OpenNN;

class MASNeuralNetwork : public NeuralNetwork
{
public:

    // Input

    void add_input(const size_t&);
    void add_input(const size_t&, const size_t&);
    void add_input(const size_t&, const size_t&, const size_t&);

    void construct_inputs(void);

    // Parameters

    size_t count_parameters_number(void) const;
    Vector<double> arrange_parameters(void) const;

    void set_parameters(const Vector<double>&);

    // Output

    void add_output(const size_t&);
    void construct_outputs(void);

    Vector<double> calculate_outputs(const Vector<double>&) const;
    Matrix<double> calculate_output_data(const Matrix<double>&) const;

    // Serialization methods

    void save(const std::string&) const;

    virtual void load(const std::string&);

protected:

    // MEMBERS

    /// Inputs layers for pars, date-time data and others data.

    Vector< Vector<PerceptronLayer*> > inputs_layers_pointers;

    /// Main layers

    //MultilayerPerceptron* multilayer_perceptron_pointer;

    /// Outputs layers for forecasting pars;

    Vector<PerceptronLayer*> outputs_layers_pointers;

    /// Saved data for recurent layers

    Vector< Vector<double> > memory_outputs_data;
};



#endif // MASOPENNNCLASSES_H
