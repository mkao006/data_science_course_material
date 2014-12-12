SELECT COUNT(*) 
       FROM (
       	    SELECT DISTINCT(docid)
       	    	   FROM Frequency 
       		   GROUP BY docid
       		   HAVING SUM(count) > 300
       ) x;

