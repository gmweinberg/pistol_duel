#!/usr/bin/env python

"""Claude-generated code to use sympy to create a sampling function"""
import numpy as np
import sympy as sp

def derive_sampling_function(pdf_expr, x, domain):
    # Calculate the CDF
    cdf = sp.integrate(pdf_expr, (x, domain[0], x))
    
    # Solve for the inverse CDF
    y = sp.Symbol('y')
    # Choose the solution that's within the domain

    inverse_cdf_solutions = sp.solve(sp.Eq(cdf, y), x)
    print(inverse_cdf_solutions)
    good_sampling_func = None
    for sol in inverse_cdf_solutions:
        sampling_func = sp.lambdify(y, sol, modules="numpy")
        if sampling_func(0.5) >= domain[0] and  sampling_func(0.5) <= domain[1]:
            print(f"CDF: {cdf}")
            print(f"Inverse CDF: {sol}")
            good_sampling_func = sampling_func

    if good_sampling_func is None:
        raise ValueError("Couldn't find a valid inverse CDF within the domain")
    
    
    # Create a lambda function for sampling
    # sampling_func = sp.lambdify(y, inverse_cdf, modules="numpy")
    
    return lambda size=1: sampling_func(np.random.uniform(0, 1, size))

if  __name__ == '__main__':
    # Example usage
    x = sp.Symbol('x')
    pdf_expr = 1 / (4 * x**3)
    domain = (1/3, 1)

    sample_func = derive_sampling_function(pdf_expr, x, domain)

    # Test the function
    samples = sample_func(10000)
    print(f"Mean of samples: {np.mean(samples)}")
    print(f"Min of samples: {np.min(samples)}")
    print(f"Max of samples: {np.max(samples)}")
