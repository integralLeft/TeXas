# TeXas (OUTDATED)

Discord bot to render LaTeX and solve equations. 

## Dependencies

* sympy
* pdflatex
* dotenv
* pdfcrop
* imagemagick
* python

## Usage

> latex `x`

...where `x` is some LaTeX, will render `x` as LaTeX.

> solve `x`

...where `x` is some valid expression, or valid SymPy expression, will render the solution to that expression in LaTeX.

### Examples

> latex \frac{1}{\sqrt{2\pi}} \int_{-\infty}^\infty e^{-\frac{x^2}{2}} \text{d}x

> solve integrate(E**(-x**2/2)/sqrt(2*pi),(x,-oo,oo))


