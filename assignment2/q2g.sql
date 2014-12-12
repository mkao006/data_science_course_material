SELECT value
       FROM (
       	    SELECT A.row_num, B.col_num, sum(a.value * b.value) as value
       	    	   FROM A JOIN B ON A.col_num == B.row_num
       		   GROUP BY A.row_num, B.col_num
       ) x
       WHERE row_num == 2 AND col_num == 3;
