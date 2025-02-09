int parsefile(const char* fname, long int* data, int* par_inputs, int* par_outputs)
{
    using namespace std;

    unsigned int inputs = 0;
    unsigned int outputs = 0;
    FILE    *fh = NULL;
    long int     *temp = NULL;
    char    ch;   
    long int     tmpval;
    int     rpoc = 0; //number of read bits
    int     lineno = 1; 
    bool    inputpart = true;
    int     datarows = 0;
    string  sinps, soutps;

#define flushbuf() \
  for (unsigned int i=0; i < inputs+outputs; i++) { \
      if (data) { data[datarows] = temp[i];} \
      if (!data) printf("%d:%016lX\n", datarows, temp[i]); \
      datarows++; \
  }

    if (!(fh = fopen(fname,"r"))) {fprintf(stderr, "File '%s' not found\n", fname); return -1; }
    do {
       ch = getc(fh);
       if (ch == '#') {
          while ((ch != '\n') && ((ch = getc(fh)) != EOF));
       } else if (isspace(ch)) {
          while ((ch != '\n') && ((ch = getc(fh)) != EOF) && (isspace(ch)));
          if (ch != '\n')
             ungetc(ch, fh);
       } else if (ch == ':') {
          inputpart = !inputpart;
       } else if (ch != EOF) {
          if ((ch != '0') && (ch != '1')) {
             fprintf(stderr,"line %d: Invalid character",lineno);
             return -1;
          }
          if (inputpart) { //cte se vstupni kombinace
             sinps += ch;
          } else { //cte se vystupni kombinace
             soutps += ch;
          }
       }

       if ((!inputpart) && ((ch == '\n') || (ch == EOF))) 
       {
          inputpart = true;
          if ((sinps != "") && (soutps != "")) 
          {
                  
             if (rpoc == 0) 
             { 
                //pri nacteni prvni radky se musi alokovat temp
                inputs = sinps.length();
                outputs = soutps.length();
                if ((inputs == 0) || (outputs == 0)) {
                   fprintf(stderr,"line %d: Invalid number of inputs / outputs\n",lineno);
                   return -1;
                }
                temp = new long int [inputs + outputs];
             }

             if ((inputs != sinps.length()) || (outputs != soutps.length())) {
                fprintf(stderr,"line %d: The number of inputs/outputs do not match the previous lines\n",lineno);
                return -1;
             }

             for (unsigned int i=0; i < inputs; i++) {
                tmpval = sinps[i] - 48;
                temp[i] = ((temp[i] >> 1) & 0x7fffffffffffffffL) | (tmpval*0x8000000000000000L);
             }
             for (unsigned int i=0; i < outputs; i++) {
                tmpval = soutps[i] - 48;
                temp[i+inputs] = ((temp[i+inputs] >> 1) & 0x7fffffffffffffffL) | (tmpval*0x8000000000000000L);
             }

             if (rpoc % 64 == 63) { //pokud je temp integeru naplneno, musi se vypsat
                flushbuf();
             }

             rpoc++;
             sinps = "";
             soutps = "";
          }
          lineno++;
       }
    } while (ch != EOF);

    if ((rpoc >0) && (rpoc % 64 != 0))  
    {  // je-li temp nezaplneno je treba doplnit do 32 bitu
       int imax = (64 - (rpoc % 64));      // posledni zapsanou bitovou kombinaci
       for (int i=0; i < imax; i++)
          for (unsigned int j=0; j < inputs+outputs; j++) {
              tmpval = temp[j] & 0x8000000000000000L;
              temp[j] = ((temp[j] >> 1) & 0x7fffffffffffffffL) | (tmpval);
          }
       flushbuf();
    }

    if (temp != NULL)
       delete[] temp;

    fclose(fh);

    if (par_inputs != 0) *par_inputs = inputs;
    if (par_outputs != 0) *par_outputs = outputs;

    return datarows;
}
