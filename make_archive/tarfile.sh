#!/bin/bash

cd /eos/user/a/aman/LHCDM_tchan_Combination/output2_old/

tar -czf output_u_S3M.tar.gz output_u_S3M/
tar -czf output_d_S3M.tar.gz output_d_S3M/
tar -czf output_s_S3M.tar.gz output_s_S3M/

tar -czf output_u_F3S.tar.gz output_u_F3S/
tar -czf output_d_F3S.tar.gz output_d_F3S/
tar -czf output_s_F3S.tar.gz output_s_F3S/

tar -czf output_u_F3V.tar.gz output_u_F3V/
tar -czf output_d_F3V.tar.gz output_d_F3V/
tar -czf output_s_F3V.tar.gz output_s_F3V/