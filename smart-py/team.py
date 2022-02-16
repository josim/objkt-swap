
import smartpy as sp

class Team(sp.Contract):
    """This contract implements the first version of the SatireBall Game.

    """

    TEAM_TYPE = sp.TRecord(
    # The user that created the team
    issuer=sp.TAddress,
    # The player ids
    player_ids=sp.TNat).layout(
        ("issuer", ("player_ids")))

    
    def __init__(self, manager, metadata):
        """Initializes the contract.
        Parameters
        ----------
        manager: sp.TAddress
            The initial marketplace manager address. It could be a tz or KT
            address.
        metadata: sp.TBigMap(sp.TString, sp.TBytes)
            The contract metadata big map. It should contain the IPFS path to
            the contract metadata json file.
        """
        # Define the contract storage data types for clarity
        self.init_type(sp.TRecord(
            # The contract manager. It could be a tz or KT address.
            manager=sp.TAddress,
            # The contract metadata bigmap.
            # The metadata is stored as a json file in IPFS and the big map
            # contains the IPFS path.
            metadata=sp.TBigMap(sp.TString, sp.TBytes),
            # The big map with the swaps information.
            teams=sp.TBigMap(sp.TAddress, Team.TEAM_TYPE),
            # The swaps bigmap counter. It tracks the total number of swaps in
            # the swaps big map.
            counter=sp.TNat,
            # The proposed new manager address. Only set when a new manager is
            # proposed.
            proposed_manager=sp.TOption(sp.TAddress),
            # A flag that indicates if the marketplace set_team is paused or not.
            team_paused=sp.TBool,

        # Initialize the contract storage
        self.init(
            manager=manager,
            metadata=metadata,
            teams=sp.big_map(),
            counter=0,
            proposed_manager=sp.none,
            teams_paused=False)
          
    def check_is_manager(self):
        """Checks that the address that called the entry point is the contract
        manager.
        """
        sp.verify(sp.sender == self.data.manager, message="MP_NOT_MANAGER")
          
          
          
    @sp.entry_point
    def set_team(self, params):
        """Every Team contains 11 Players

        Parameters
        ----------
        params: sp.TRecord
            The team parameters:
            - player_ids: the player ids.
            - creator: the artist/creator address.
        """
        # Check that teams are not paused
        sp.verify(~self.data.teams_paused, message="MP_TEAMS_PAUSED")
          
        # Check if User is in posession of player tokens
        sp.if self.data.teams[sp.sender] != sp.sender:
            sp.for token_id in params.token_ids:
                self.data.teams[sp.sender].player_ids = params.token_id
        # Update the teams bigmap with the new team information
        self.data.teams[sp.sender] = sp.record(
            issuer=sp.sender,
            player_ids=params.player_ids)

        
