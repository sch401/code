/*   dx.doi.org/10.1021/ie100980n   */

#include "udf.h"
#include "mem.h"
#include "sg_mphase.h"
#include "math.h"
#define diam2 0.00038
#define fai 0.8735
DEFINE_EXCHANGE_PROPERTY(clift, cell, mix_thread, s_col, f_col)
{
    Thread *thread_l, *thread_s;
    real x_vel_l, x_vel_s, y_vel_l, y_vel_s, z_vel_l, z_vel_s, abs_v, slip_x, slip_y, slip_z, rho_l,
        mu_l, void_l, reyp, cd, k_l_s, Asurf, fshape, Cshape, reyp1, void_s, cons1, cons2, cons3;
    thread_l = THREAD_SUB_THREAD(mix_thread, s_col);
    thread_s = THREAD_SUB_THREAD(mix_thread, f_col);
    x_vel_l = C_U(cell, thread_l);
    y_vel_l = C_V(cell, thread_l);
    z_vel_l = C_W(cell, thread_l);
    x_vel_s = C_U(cell, thread_s);
    y_vel_s = C_V(cell, thread_s);
    z_vel_s = C_W(cell, thread_s);
    slip_x = x_vel_s - x_vel_l;
    slip_y = y_vel_s - z_vel_l;
    slip_z = z_vel_s - z_vel_l;
    rho_l = C_R(cell, thread_l);
    mu_l = C_MU_L(cell, thread_l);
    abs_v = sqrt(slip_x * slip_x + slip_y * slip_y + slip_z * slip_z);
    void_l = C_VOF(cell, thread_l);
    void_s = C_VOF(cell, thread_s);

    Asurf = 1.0 / fai;

    fshape = 1.0 / 3.0 + 2.0 / 3.0 * (1.0 / sqrt(fai));
    Cshape = 1.0 + 0.7 * sqrt(Asurf - 1) + 2.4 * (Asurf - 1);
    reyp = rho_l * abs_v * diam2 / mu_l;
    reyp1 = Cshape * reyp / fshape;
    cons1 = pow(void_l * reyp1, 0.687);
    cons2 = pow(void_l * reyp1, 1.16);
    cd = 24.0 / (void_l * reyp1) * (1.0 + 0.15 * cons1) + 0.42 / (1.0 + 42500 / cons2);
    cons3 = pow(void_l, -2.65);
    k_l_s = 0.75 * (1 - void_l) * void_l * rho_l * cd * abs_v * cons3 / diam2;
    return k_l_s;
}
