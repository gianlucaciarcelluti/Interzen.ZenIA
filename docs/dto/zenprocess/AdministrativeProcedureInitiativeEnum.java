package it.interzen.zencommonlibrary.dto.zenprocess;

public enum AdministrativeProcedureInitiativeEnum {
	YES("YES"), NO("NO");
	
	public final String label;

    private AdministrativeProcedureInitiativeEnum(String label) {
        this.label = label;
    }
}
