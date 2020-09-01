function b = sintr(f)% b = sintr(f)% Discrete Sine Transform% given values f=[f_1,...,f_{N-1}] at x=1/N,...,(N-1)/N % (NOTE: endpoints are NOT included)% find coefficients b=[b_1,...,b_{N-1}] % of sine series sum_{k=1...N-1} b_k sin(k*pi*x)% f MUST be a COLUMN VECTOR, b will also be a column vector% If f is an array the transform acts on each column, % and b is an array of the same sizeN = size(f,1) + 1;% odd extension of each column of length n=N-1 to length 2*NG = [0;f;0;-f(end:-1:1)];% apply four() to each columnGh = fft(G,2*N,1)/(2*N);b = 1i*(Gh(2:N)-Gh(end:-1:N+2));b = real(b); % this should not change b in theory.  It should be all real.