
from akit.mixins.scope import IteratorScopeMixIn
from akit.mixins.automationpodmixin import AutomationPodMixIn



class ListIterationContext:

    def __init__(self, iterable_list):
        self._iterable_list = iterable_list
        self._next_index = 0
        return

    @property
    def current_item(self):
        return self._iterable_list[self._next_index]

    def advance(self):
        self._next_index += 1

        if self._next_index >= len(self._iterable_list):
            raise StopIteration("No more items")

        return

class PlaybackDevicesIteratorMixIn(IteratorScopeMixIn, AutomationPodMixIn):

    @classmethod
    def iteration_initialize(cls):
        """
            This API is overridden by derived iterator scope mixins and is called by the sequencer at the start
            of the use of a scope before the scope is entered for the first time.  It provides a hook for the
            iteration scope to setup the iteration state for the iteration scope.
        """
        device_list = []
        iterctx = ListIterationContext(device_list)
        return iterctx
    
    @classmethod
    def iteration_advance(cls, iterctx):
        """
            The 'iteration_advance' API is overridden by derived iterator scope mixins and is called by the
            sequencer after the scope exits.  This class level hook method is used by the sequencer to advance
            the scope to the next iteration state.  The 'iteration_advance' API will return a 'True' result
            when the advancement of the iteration state was successful and the scope can be re-entered for
            execution.  The 'iteration_advance' API will return a 'False' when the advancement of the iteration
            state has reached the end of its iteration cycle and the scope should not be re-entered.
        """
        iterctx.next()
        return

    @classmethod
    def scope_enter(cls):
        """
            This API is called by the sequencer when a scope of state is being entered by an automation
            run.  The derived `ScopeMixIn` implementation should initialize the scope they are designed
            to manage and if initialization fails, they should raise a :class:`akit.exceptions.AKitScopeEntryError`
            error.

            :raises :class:`akit.exceptions.AKitScopeEntryError`:
        """
        return

    @classmethod
    def scope_exit(cls):
        """
            This API is called by the sequencer when an automation run is exiting a scope.  The derived
            ScopeMixIn implementation should use this opportunity to tear down the scope that it is
            managing.
        """
        return
