SELECT value
       FROM (
       	    SELECT docid, sum(count) as value
       	    	   FROM Frequency
       	    	   WHERE term IN ("washington", "taxes", "treasury")
		   GROUP BY docid
       ) x
       ORDER BY value DESC
       LIMIT 1;
