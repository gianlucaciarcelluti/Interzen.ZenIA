package it.interzen.zencommonlibrary.dto.zenadmin;

import java.util.Date;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ResultLicenseDTO {
	 private long id;
     private String description;
     private String microservice;
	 private Long accessNumber;
	 private boolean isLicense;
	 private Long userid;
	 private int totlicensesused;
	 private Date effectiveDate;
     private Date expirationDate;
     private Integer accessType;
     private Integer diskQuote;
     private Integer documentNumber;
     private Integer companyNumber;
}
