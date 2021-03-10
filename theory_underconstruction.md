# Theory


## Green's function

$$
 G^\sigma(\mathbf{r},\mathbf{r}',\omega) =
 \sum_i \frac{ \varphi_i^\sigma(\mathbf{r}) \varphi_i^\sigma(\mathbf{r'})}
  { \omega - \epsilon_i^\sigma - \mathrm{i} \eta}
   +
 \sum_a \frac{ \varphi_a^\sigma(\mathbf{r}) \varphi_a^\sigma(\mathbf{r'})}
  { \omega - \epsilon_a^\sigma + \mathrm{i} \eta}
$$

## Linear combination of atomic orbitals (LCAO)

$$
 \varphi_n^\sigma(\mathbf{r}) = \sum_\mu C_{\mu n}^\sigma \phi_\mu(\mathbf{r}) 
$$

where $\phi_\mu(\mathbf{r})$ are Gaussian-Type Orbital centered on atom $\mathbf{R_A}$

$$
  \phi_\mu(\mathbf{r}) 
   = \mathcal{Y}_{lm}(\widehat{ \mathbf{r - R_A}}) \left| \mathbf{r-R_A}\right|^l
     \sum_b c_{ b}
        e^{ -\alpha_{b} \left| \mathbf{r-R_A}\right|^2 } 
$$




## AO to MO transform

This scales formally as $N^4$:

$$
  ( P | p q ) = \sum_\alpha  C_{\alpha p}  \left[ \sum_\beta  C_{\beta q} ( \alpha \beta | P ) \right]
$$


## Polarizability for imaginary frequencies

$$
 (v^{1/2} \chi_0 v^{1/2})_{PQ}(\mathrm{i}\omega) = \sum_{ia}  ( P | i a ) ( Q | i a ) 
     \left[ \frac{1}{\mathrm{i} \omega - \epsilon_a + \epsilon_i}
          - \frac{1}{\mathrm{i} \omega - \epsilon_i + \epsilon_a} 
     \right]
$$


$$
 (v^{1/2} \chi v^{1/2})_{PQ}(\mathrm{i}\omega)
      =
 (v^{1/2} \chi_0 v^{1/2})_{PQ}(\mathrm{i}\omega)
   + \sum_{R}
 (v^{1/2} \chi_0 v^{1/2})_{PR}(\mathrm{i}\omega)
 (v^{1/2} \chi_0 v^{1/2})_{RQ}(\mathrm{i}\omega)
$$

$$
 (v^{1/2} \chi v^{1/2})_{PQ}(\mathrm{i}\omega)
   =
  \sum_R
 (v^{1/2} \chi_0 v^{1/2})_{PR}(\mathrm{i}\omega)
  \left[
    I - v^{1/2} \chi_0 v^{1/2}(\mathrm{i}\omega)
  \right]^{-1}_{RQ}
$$
