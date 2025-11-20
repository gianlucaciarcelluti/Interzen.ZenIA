package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.exception.ZenRestApiException;
import lombok.Getter;

@Getter
public enum ZenMicroservices {	
	ZenAdmin(0, "msazenadmin"),
	ZenDocuments(1, "msazendocuments"),
	ZenMaster(2, "msazenmaster"),
	ZenProtocollo(3, "msazenprotocollo"),
	ZenMailRoom(4, "msazenmailroom"),
	ZenGateway(5, "msacloudgateway"),
	ZenProcess(5, "msazenprocess"),
	ZenArchive(6, "msazenarchive"),
	GhostZenGovernance(7,"msazengovernance"),
	ZenSuap(8,"msazensuap"),
	GhostZenSecurity(9,"msazensecurity"),
	GhostZenDocumentCreation(10,"msazendocumentcreation");
	
	ZenMicroservices(long id, String s) {
		description = s;
		this.id = id;
	}
	
	public String toString() {
		return description;
	}

	
	public static ZenMicroservices getZenMicroservices(long id) {
		for(var m:ZenMicroservices.values()) {
			if (id == m.getId()) {
				return m;
			}
		}
		
		throw new ZenRestApiException("id non tradotto in ZenMicroservices " + id);
	}
	
	String description;
	long id;
}
