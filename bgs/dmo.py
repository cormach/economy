from dataclasses import dataclass, Field


@dataclass
class ThreeMonthLagLinker:
    """
    Represents a ThreeMonthLagLinker with a field for the name.
    """

    w: float = Field(name="The real discount factor for a semiannual period")
    r: int = Field(
        name="""
        The number of calendar days from settlement date to the next quasi-coupon date 
        (r=s if the settlement date falls on quasi-coupondate)"""
    )
    s: int = Field(
        name="""
                 The number of calendar days in the full quasi-coupon period in which the settlement date occurs
                 (i.e. between the prior quasi-coupon date and the following quasi-coupon date)"""
    )
    n: int = Field(
        name="""
                  The number of full quasi-coupon periods from the nex quasi-coupon
                  period after the settlement date to the redemption date
                  """
    )
    rho: float = Field(
        name="""
                       Semi-annually compounded real redemption yield, i.e. if the real yield is 2.5% then rho=0.025"""
    )
