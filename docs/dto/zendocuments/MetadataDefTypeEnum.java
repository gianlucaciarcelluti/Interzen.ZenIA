package it.interzen.zencommonlibrary.dto.zendocuments;

public enum MetadataDefTypeEnum {
	TEXT(1, "Text"),
	TEXTAREA(2, "Textarea"),
	LOOKUP(3, "Lookup"),
	MULTILOOKUP(4, "MultiLookup"),
	FLOAT(5, "Float"),
	CURRENCY(6, "Currency"),
	DATE(7, "Date"),
	EXPIRATION(8, "Expiration"),
	DATETIME(9, "DateTime"),

	COUNTER(10, "Counter"),
	COUNTERYEAR(11, "CounterYear"),
	INTEGER(12, "CounterYear");
		
	int id;
	String description;
	
	MetadataDefTypeEnum(int id, String description) {
		this.id = id;
		this.description = description;
	} 
}
