package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

public enum AssignmentSlaveActionStatus {
	NEW, COMPETENCE_ACCEPTED, FINAL_COMPETENCE_WORKED, FINAL_NOTIFICATION_VIEWED, FINAL_REFUSED;
	
	
	
	public static boolean isFinalStatus(AssignmentSlaveActionStatus actualStatus) {
		if (actualStatus == FINAL_COMPETENCE_WORKED || actualStatus == FINAL_NOTIFICATION_VIEWED
				|| actualStatus == FINAL_REFUSED) {
			return true;
		}
		return false;
	}
}
