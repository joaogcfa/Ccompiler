{
    x = 3;
    y = 2;
    x_2 = 7;
    y_2 = 5;

    z = x + y;
    z_2 = x_2 + y_2;
    printf(x);
    printf(z);
    printf(z_2);
    printf(x - -y);

    w = (x + y) / y_2;
    printf(/* bla */ w /* bla */);
    /*bla bla
    bla
    bla */

    printf(w + x);
    b = w + x_2;
    printf(b + w + z);
}