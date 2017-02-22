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
    size_t get_inputs_number(void);

    // Parameters

    size_t count_parameters_number(void) const;
    Vector<double> arrange_parameters(void) const;

    void set_parameters(const Vector<double>&);

    // Output

    void add_output(const size_t&);
    void construct_outputs(void);
    size_t get_outputs_number(void);

    Vector<double> calculate_outputs(const Vector<double>&) const;
    Matrix<double> calculate_output_data(const Matrix<double>&) const;

    // Serialization methods

    void save(const std::string&) const;

    virtual void load(const std::string&);

protected:

    // MEMBERS

    /// Inputs layers for pars, date-time data and others data.

    Vector< Vector<PerceptronLayer*> > inputsArrayPtr;

    /// Main layers

    //MultilayerPerceptron* multilayer_perceptron_pointer;

    /// Outputs layers for forecasting pars.

    Vector<PerceptronLayer*> outputsArrayPtr;

    /// Saved data for recurent layers.

    Vector< Vector< Vector<double> > > memoryHistoryData;
};

class RecurrentPerceptronLayer : public PerceptronLayer
{
public:
    explicit RecurrentPerceptronLayer();
    explicit RecurrentPerceptronLayer();

protected:

};

class LstmPerceptronLayer : public PerceptronLayer
{
public:

    // ENUMERATIONS

    /// Type of implementation a recurrent LSTM layer.

    enum Type{Standart, PeepholeConnections, GatedRecurrentUnit};


protected:

};

#endif // MASOPENNNCLASSES_H
