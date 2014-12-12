SELECT COUNT(DISTINCT(docid))
       FROM (
       SELECT docid
       	      FROM Frequency
	      WHERE term == "transactions"
       INTERSECT
       SELECT docid
       	      FROM Frequency
	      WHERE term == "world"
       )x;
